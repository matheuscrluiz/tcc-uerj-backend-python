import pandas as pd
from ...util.exceptions import DAOException
from ..base import tcc_dao_base as base


class CheckinDAO(base.DAOBase):

    def __init__(self):
        super().__init__()

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def get_checkin(self, id: int = None) -> dict:

        try:
            rotina = 'get_checkin'
            query = """
                select id, reserva_id, hora_checkin, hora_checkout, status,
                       data_inclusao, data_alteracao,
                       ch_usuario_inclusao, ch_usuario_alteracao
                from checkin
            """

            parms_oracle = {}

            if id is not None:
                query += " where id = %(id)s"
                parms_oracle["id"] = id

            query += " order by id"

            dataframe = pd.read_sql(
                sql=query, con=self.get_connection(), params=parms_oracle)

            return self.convert_dataframe_to_dict(dataframe)

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)

    def add_checkin(self, parm_data: dict) -> int:

        try:
            rotina = 'add_checkin'

            cmdSql = """
                INSERT INTO checkin
                    (reserva_id, hora_checkin, hora_checkout, status, ch_usuario_inclusao)
                VALUES
                    (%(reserva_id)s, %(hora_checkin)s, %(hora_checkout)s,
                     %(status)s, %(ch_usuario_inclusao)s)
                RETURNING id;
            """

            parms_oracle = {
                "reserva_id": parm_data["reserva_id"],
                "hora_checkin": parm_data.get("hora_checkin"),
                "hora_checkout": parm_data.get("hora_checkout"),
                "status": parm_data["status"],
                "ch_usuario_inclusao": parm_data.get("ch_usuario_inclusao", "SISTEMA")
            }

            new_id = self.execute_dml_command_parms(cmdSql, parms_oracle)

            return new_id

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)

    def update_checkin(self, parm_data: dict):

        try:
            rotina = 'update_checkin'
            cmdSql = """
                update checkin
                    set hora_checkin = %(hora_checkin)s,
                        hora_checkout = %(hora_checkout)s,
                        status = %(status)s,
                        data_alteracao = CURRENT_TIMESTAMP,
                        ch_usuario_alteracao = %(ch_usuario_alteracao)s
                    where id = %(id)s
            """
            parms_oracle = {
                "id": parm_data["id"],
                "hora_checkin": parm_data.get("hora_checkin"),
                "hora_checkout": parm_data.get("hora_checkout"),
                "status": parm_data["status"],
                "ch_usuario_alteracao": parm_data.get("ch_usuario_alteracao", "SISTEMA")
            }

            self.execute_dml_command_parms(cmdSql, parms_oracle)

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)

    def remove_checkin(self, id: int):

        try:
            rotina = 'remove_checkin'
            cmdSql = """
                delete from checkin
                where id = %(id)s
            """

            parms_oracle = {
                "id": id
            }

            self.execute_dml_command_parms(cmdSql, parms_oracle)

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)
