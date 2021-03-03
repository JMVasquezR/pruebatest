from core.auth_methods.ssh import UserPasswordAuthMethod
from core.connectors import SshConnector
from core.scripts.simple_flow import SimpleScript


class TestScript(SimpleScript):
    CONNECTOR_CLASS = SshConnector
    AUTH_METHOD_CLASS = UserPasswordAuthMethod
    SCRIPT_PARAMS_DICT = {}

    def validate(self):
        return True

    def run(self):
        print('ingreso')
        return True
