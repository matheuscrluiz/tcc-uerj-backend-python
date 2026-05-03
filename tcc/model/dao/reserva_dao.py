import pandas as pd
from ...util.exceptions import DAOException
from ..base import tcc_dao_base as base


class ReservaDAO(base.DAOBase):

    def __init__(self):
        super().__init__()

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def get_reserva(self, id: int = None) -> dict:

        try:
            rotina = 'get_reserva'
            query = """
                select id, usuario_id, estacao_id, data, hora_inicio,
                    hora_fim, status, data_inclusao, data_alteracao,
                       ch_usuario_inclusao, ch_usuario_alteracao
                from reserva
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

    def add_reserva(self, parm_data: dict) -> int:

        try:
            rotina = 'add_reserva'

            cmdSql = """
                INSERT INTO reserva
                    (usuario_id, estacao_id, data, hora_inicio,
                      hora_fim, status, ch_usuario_inclusao)
                VALUES
                    (%(usuario_id)s, %(estacao_id)s, %(data)s,
                      %(hora_inicio)s, %(hora_fim)s,
                     %(status)s, %(ch_usuario_inclusao)s)
                RETURNING id;
            """

            parms_oracle = {
                "usuario_id": parm_data["usuario_id"],
                "estacao_id": parm_data["estacao_id"],
                "data": parm_data["data"],
                "hora_inicio": parm_data["hora_inicio"],
                "hora_fim": parm_data["hora_fim"],
                "status": parm_data["status"],
                "ch_usuario_inclusao": parm_data["ch_usuario_inclusao"]
            }

            new_id = self.execute_dml_command_parms(cmdSql, parms_oracle)

            return new_id

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)

    def update_reserva(self, parm_data: dict):

        try:
            rotina = 'update_reserva'
            cmdSql = """
                update reserva
                    set hora_inicio = %(hora_inicio)s,
                        hora_fim = %(hora_fim)s,
                        status = %(status)s,
                        data_alteracao = CURRENT_TIMESTAMP,
                        ch_usuario_alteracao = %(ch_usuario_alteracao)s
                    where id = %(id)s
            """
            parms_oracle = {
                "id": parm_data["id"],
                "hora_inicio": parm_data["hora_inicio"],
                "hora_fim": parm_data["hora_fim"],
                "status": parm_data["status"],
                "ch_usuario_alteracao": parm_data["ch_usuario_alteracao"]
            }

            self.execute_dml_command_parms(cmdSql, parms_oracle)

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)

    def remove_reserva(self, id: int):

        try:
            rotina = 'remove_reserva'
            cmdSql = """
                delete from reserva
                where id = %(id)s
            """

            parms_oracle = {
                "id": id
            }

            self.execute_dml_command_parms(cmdSql, parms_oracle)

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)
