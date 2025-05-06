import os
import hvac

VAULT_ADDR = os.getenv("VAULT_ADDR")
VAULT_ROLE_ID = os.getenv("VAULT_ROLE_ID")
VAULT_SECRET_ID = os.getenv("VAULT_SECRET_ID")
VAULT_MOUNT = os.getenv("VAULT_MOUNT", "secrets")


class VaultClient:
    def __init__(self):
        self.client = hvac.Client(url=VAULT_ADDR)
        self._authenticate()

    def _authenticate(self):
        print()
        self.client.auth.approle.login(
            role_id=VAULT_ROLE_ID,
            secret_id=VAULT_SECRET_ID
        )
        if not self.client.is_authenticated():
            raise Exception("Vault AppRole authentication failed")

    def read_secret(self, path: str) -> dict:
        response = self.client.secrets.kv.v2.read_secret_version(
            path=path,
            mount_point=VAULT_MOUNT,
            raise_on_deleted_version=True
        )
        return response['data']
