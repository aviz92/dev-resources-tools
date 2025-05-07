import logging
import os
import hvac


class VaultClient:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.vault_addr = os.getenv("VAULT_ADDR")
        self.vault_role_id = os.getenv("VAULT_ROLE_ID")
        self.vault_secret_id = os.getenv("VAULT_SECRET_ID")
        self.vault_mount = os.getenv("VAULT_MOUNT", "secrets")

        self.client = hvac.Client(url=self.vault_addr)
        self._authenticate()

    def _authenticate(self):
        print()
        self.client.auth.approle.login(
            role_id=self.vault_role_id,
            secret_id=self.vault_secret_id
        )
        if not self.client.is_authenticated():
            raise Exception("Vault AppRole authentication failed")

    def read_secret(self, path: str) -> dict:
        response = self.client.secrets.kv.v2.read_secret_version(
            path=path,
            mount_point=self.vault_mount,
            raise_on_deleted_version=True
        )
        return response['data']
