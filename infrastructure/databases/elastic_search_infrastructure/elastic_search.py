import logging
import datetime
import time
from enum import Enum
from typing import Any
import pandas as pd
from copy import deepcopy
from elasticsearch import helpers

from databases.elastic_search_infrastructure.elastic_serach_connection import ElasticSearchOnPremConnection, \
    ElasticSearchCloudConnection


class ElasticSearchConnectionType(Enum):
    ELASTICSEARCH_ON_PREM = ElasticSearchOnPremConnection
    ELASTICSEARCH_CLOUD = ElasticSearchCloudConnection


class ElasticSearch:
    def __init__(self, elk_client_type: ElasticSearchConnectionType):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.elk_client = elk_client_type.value()
        self.doc = {}

    def fill_list_of_docs(
        self,
        list_of_docs: list[dict],
        index_name: str,
        doc: dict[str, Any]
    ) -> None:
        list_of_docs.append(
            {
                "_index": index_name,
                "_source": deepcopy(doc)
            }
        )

    def set_list_of_docs(self, list_of_docs: list[dict], request_timeout: int = 600, quick: bool = True) -> None:
        self.logger.info('Start to report the documents to ELK')

        if quick:
            if failed_response := helpers.streaming_bulk(
                self.elk_client,
                list_of_docs,
                raise_on_error=False,
                request_timeout=request_timeout,
                chunk_size=1000
            ):
                for item in failed_response:
                    if item[1]['index']['status'] != 201 or item[1]['index']['_shards']['failed'] > 0:
                        self.logger.debug(f'Failed document: \n{item}')
        else:
            success_response, failed_response = helpers.bulk(self.elk_client, list_of_docs)
            if success_response == len(list_of_docs):
                self.logger.info('All documents were reported successfully')
            else:
                self.logger.error(
                    f'Not all documents were reported successfully.\n The documents that were not reported successfully: {failed_response}')
        self.logger.info('Finish to report the documents to ELK')

    def fill_elk_index_as_bulk_chunk(self, list_of_docs: list[dict], chunk_size=1000, time_sleep: int = 60) -> None:
        for i in range(0, len(list_of_docs), chunk_size):
            self.logger.info(f'index: {i} - {i + chunk_size} / {len(list_of_docs)}')
            chunk = list_of_docs[i:i + chunk_size]
            self.set_list_of_docs(list_of_docs=chunk)
        time.sleep(time_sleep)

    def fill_elk_index_as_bulk(
        self,
        data: list[dict],
        doc_id: str,
        doc_index_name: str,
        timestamp: datetime,
        date_and_time: str,
        username: str = None,
        chunk_size=1000,
        time_sleep: int = 1
    ) -> None:
        list_of_docs = []
        for index, row in enumerate(data):
            self.logger.debug(f'index: {index + 1}/{len(data)}')

            self.doc = {}
            self.add_basic_info(
                doc_id=doc_id,
                timestamp=timestamp,
                date_and_time=date_and_time,
                username=username,
            )

            for custom_field, value in row.items():
                self.doc[custom_field] = value
                self.add_list_values_as_str(value=value, column=custom_field)
            self.fill_list_of_docs(list_of_docs=list_of_docs, index_name=doc_index_name, doc=self.doc)
        self.fill_elk_index_as_bulk_chunk(list_of_docs=list_of_docs, chunk_size=chunk_size, time_sleep=time_sleep)

    def add_basic_info(self, doc_id: str, timestamp: datetime, date_and_time: str, username: str = None) -> None:
        self.doc.update(
            {
                'doc_id': doc_id,
                'timestamp': timestamp,
                'date_str': f'{date_and_time}'.replace('-', '_')
            }
        )

        if username:
            self.doc['username'] = username

    def add_list_values_as_str(self, value: any, column: str) -> None:
        if type(value) is list and not pd.isnull(all(value)) and all(type(item) is str for item in value):
            value = list(filter(lambda item: item is not None, value))
            self.doc[f'{column}'] = value
            self.doc[f'{column}_str'] = ', '.join(value)

    def convert_dataframes_to_list_of_docs(self, dataframe: pd.DataFrame) -> list:
        data = []
        dataframe_values = dataframe.values.tolist()
        for index, value in enumerate(dataframe_values):
            self.logger.debug(f'index: {index}/{len(dataframe_values)}')
            data.append(value)
        return data

    def check_if_index_exists(self, index: str) -> bool:
        if self.elk_client.indices.exists(index=index):
            self.logger.info(f"The index '{index}' exists.")
            return True
        else:
            self.logger.info(f"The index '{index}' does not exist.")
            return False

    def delete_index(self, index: str) -> None:
        self.elk_client.indices.delete(index=index)
        self.logger.info(f"The index '{index}' was deleted.")

    def check_if_index_exists_and_delete_if_exists(self, index: str) -> bool:
        if self.check_if_index_exists(index=index):
            self.delete_index(index=index)
            return True
        else:
            self.logger.info(f"The index '{index}' does not exist.")
            return False
