import hvac
from loguru import logger

from core.config import settings


class VaultClient:
    def __init__(self):
        self.client = hvac.Client(
            url=settings.VAULT_ADDR,
            token=settings.VAULT_TOKEN,
        )
        if not self.client.is_authenticated():
            raise RuntimeError("Vault authentication failed")

    def write_secret(self, user_id: str, llm_id: str, api_key: str):
        """
        Write to KV v2 at {mount}/{path}
        """
        path = f"{user_id}/{llm_id}"
        secret = dict(key=api_key)
        try:
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path, secret=secret, mount_path=settings.VAULT_KV_MOUNT_PATH
            )
        except Exception as e:
            logger.error(f"Failed to write secret to Vault: {e}")
            raise RuntimeError("Failed to write secret to Vault")

    def read_secret(self, user_id: str, llm_id: str) -> dict:
        """
        Read from KV v2 at {mount}/{path}
        """
        path = f"{settings.VAULT_KV_MOUNT_PATH}/{user_id}/{llm_id}"
        try:
            result = self.client.secrets.kv.v2.read_secret_version(
                path=path, mount_path=settings.VAULT_KV_MOUNT_PATH
            )
            return result["data"]["data"]["key"]
        except hvac.InvalidRequest as e:
            logger.error(f"Failed to read secret from Vault: {e}")
            raise RuntimeError("Failed to read secret from Vault")
        except Exception as e:
            logger.error(f"Failed to read secret from Vault: {e}")
            raise RuntimeError("Failed to read secret from Vault")
