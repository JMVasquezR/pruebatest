from core.auth_methods.ssh import PublicKeyAuthMethod
from core.connectors import SshConnector
from core.scripts.simple_flow import SimpleScript


class TestScript(SimpleScript):
    CONNECTOR_CLASS = SshConnector
    AUTH_METHOD_CLASS = PublicKeyAuthMethod
    SCRIPT_PARAMS_DICT = {}

    def run(self):
        print('ingreso')
        return True
