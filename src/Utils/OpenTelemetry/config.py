import os
import base64
from dotenv import load_dotenv

load_dotenv()


class oTelConfig:
    __username = os.getenv("GRAFANA_TRACE_USER", None)
    __password = os.getenv("GRAFANA_TRACE_PASS", None)
    url = os.getenv("GRAFANA_TRACE_URL", None)
    environment = os.getenv("GRAFANA_TRACE_ENV", "DEV")

    @staticmethod
    def get_auth_header() -> dict[str, str]:
        if oTelConfig.trace_config_provided:
            return {"authorization": f"Basic {oTelConfig.__get_basic_auth_string()}"}
        return {}

    @staticmethod
    def __get_basic_auth_string() -> str:
        if oTelConfig.trace_config_provided:
            return base64.b64encode(
                f"{oTelConfig.__username}:{oTelConfig.__password}".encode("utf-8")
            ).decode("utf-8")
        return ""

    @staticmethod
    def trace_config_provided():
        if None in [oTelConfig.__username, oTelConfig.__password, oTelConfig.url]:
            return False
        return True
