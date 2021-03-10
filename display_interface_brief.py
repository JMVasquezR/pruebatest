from typing import Optional

from core import task_status
from core.auth_methods.ssh import UserPasswordAuthMethod
from core.commands.ssh import NonUnixCommand
from core.connectors import SshConnector
from core.scripts.simple_flow import SimpleScript
from core.task_status import StatusEnum


class DisplayInterfaceBrief(SimpleScript):
    CONNECTOR_CLASS = SshConnector
    AUTH_METHOD_CLASS = UserPasswordAuthMethod
    SCRIPT_PARAMS_DICT = {}

    def __init__(self, shared_context: dict, script_params_dict: dict, connection_params_dict: dict, task_id: str):
        super().__init__(shared_context, script_params_dict, connection_params_dict, task_id)
        self._result = str

    def validate(self):
        return True

    def foo(self):
        return None

    def run(self):
        try:
            ls_result_scripts = []
            for commd in ['screen-length 0 temporary', 'display interface brief']:
                class TempCmd(NonUnixCommand):
                    DEFAULT_RESPONSE = "\n".join([commd])

                    def __init__(
                            self,
                            timeout: Optional[int] = None
                    ):
                        super().__init__(
                            cmd=self.DEFAULT_RESPONSE,
                            timeout=timeout,
                            wait_response=True
                        )

                    @property
                    def is_success(self) -> bool:
                        return True

                ls_result_scripts.append(self._connection.execute_command(TempCmd()))

            self._result = ls_result_scripts[1]
            ls_result = self._result.split('\r\n')
            indice_next = [index for index, row in enumerate(ls_result) if 'inErrors' in row]
            for index, row in enumerate(ls_result):
                if index > indice_next[0]:
                    len_row = len(row)
                    row_to_validate = row[len_row - 12:len_row]
                    if row_to_validate[0] != '0' or row_to_validate[len(row_to_validate) - 1] != '0':
                        if '>' not in row:
                            self.set_user_log(row)
            if len(self._user_log) != 0:
                self.status = StatusEnum.WARNING.value
            else:
                self.status = StatusEnum.SUCCESS.value
        except Exception as e:
            self.status = StatusEnum.FAIL.value
        return True
