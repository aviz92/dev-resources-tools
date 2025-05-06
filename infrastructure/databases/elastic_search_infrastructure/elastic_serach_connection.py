import logging
from abc import ABC, abstractmethod
from elasticsearch import Elasticsearch
from elasticsearch_dsl import connections
from retrying import retry


class ElasticSearchConnection(ABC):
    def __init__(
        self,
        elk_hostname: str,
        elasticsearch_port: int,
        kibana_port: int,
        protocol: str,
        username: str,
        password: str
    ):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._change_elasticsearch_logger()

        self.protocol = protocol
        self.elk_hostname = elk_hostname
        self.username = username
        self.password = password

        self.elasticsearch_port = elasticsearch_port
        self.elasticsearch_url = f'{self.protocol}://{self.elk_hostname}:{self.elasticsearch_port}'
        self.kibana_port = kibana_port

        self.elk_client = None

        self._change_elasticsearch_logger()

    @abstractmethod
    def _change_elasticsearch_logger(self):
        tracer = logging.getLogger('elasticsearch')
        tracer.setLevel(logging.CRITICAL)  # or desired level
        # tracer.addHandler(logging.FileHandler('indexer.log'))

    @abstractmethod
    def connect_to_elasticsearch(self):
        pass


class ElasticSearchOnPremConnection(ElasticSearchConnection):
    def __init__(
        self,
        elk_hostname: str,
        elasticsearch_port: int = 9200,
        kibana_port: int = 5602,
        protocol: str = 'http',
        username: str = None,
        password: str = None
    ):
        self.logger = logging.getLogger(self.__class__.__name__)
        super().__init__(
            elk_hostname=elk_hostname,
            elasticsearch_port=elasticsearch_port,
            kibana_port=kibana_port,
            protocol=protocol,
            username=username,
            password=password
        )

    def _change_elasticsearch_logger(self):
        super()._change_elasticsearch_logger()

    @retry(stop_max_attempt_number=3, wait_fixed=180000)
    def connect_to_elasticsearch(self):
        if self.username and self.password:
            self.elk_client = connections.create_connection(
                hosts=[self.elasticsearch_url],
                http_auth=(self.username, self.password),
                ca_certs="/etc/elasticsearch/certs/http_ca.crt",
                verify_certs=False, timeout=60
            )
        else:
            self.elk_client = connections.create_connection(hosts=[f'{self.elasticsearch_url}'], timeout=20)

        if self.elk_client.ping():
            self.logger.info("Elasticsearch on-prem Connection Successful")
        else:
            self.logger.error("Elasticsearch on-prem Connection Failed")
            raise Exception(
                f'Failed to connect to Elasticsearch on-prem on {self.elasticsearch_url}')  # sourcery skip: raise-specific-error


class ElasticSearchCloudConnection(ElasticSearchConnection):
    def __init__(
        self,
        elk_hostname: str,
        elasticsearch_port: int = 9200,
        kibana_port: int = 5602,
        protocol: str = 'http',
        username: str = None,
        password: str = None
    ):
        self.logger = logging.getLogger(self.__class__.__name__)
        super().__init__(
            elk_hostname=elk_hostname,
            elasticsearch_port=elasticsearch_port,
            kibana_port=kibana_port,
            protocol=protocol,
            username=username,
            password=password
        )

    def _change_elasticsearch_logger(self):
        super()._change_elasticsearch_logger()

    @retry(stop_max_attempt_number=3, wait_fixed=180000)
    def connect_to_elasticsearch(self):
        self.elk_client = Elasticsearch(cloud_id=self.elk_hostname, http_auth=(self.username, self.password))

        if self.elk_client.ping():
            self.logger.info("Elasticsearch cloud Connection Successful")
        else:
            self.logger.error("Elasticsearch cloud Connection Failed")
            raise Exception(
                f'Failed to connect to Elasticsearch cloud on {self.elk_hostname}')  # sourcery skip: raise-specific-error
