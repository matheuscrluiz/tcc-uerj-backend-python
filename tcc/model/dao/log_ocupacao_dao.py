import pandas as pd
from ...util.exceptions import DAOException
from ..base import tcc_dao_base as base


class LogOcupacaoDAO(base.DAOBase):

    def __init__(self):
        super().__init__()

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def get_log_ocupacao(self, id: int = None) -> dict:

        try:
            rotina = 'get_log_ocupacao'
            query = """
                select id, estacao_id, usuario_id, data, hora_inicio, hora_fim, foi_reserva,
                       data_inclusao, data_alteracao,
                       ch_usuario_inclusao, ch_usuario_alteracao
                from log_ocupacao
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

    def add_log_ocupacao(self, parm_data: dict) -> int:

        try:
            rotina = 'add_log_ocupacao'

            cmdSql = """
                INSERT INTO log_ocupacao
                    (estacao_id, usuario_id, data, hora_inicio, hora_fim, foi_reserva, ch_usuario_inclusao)
                VALUES
                    (%(estacao_id)s, %(usuario_id)s, %(data)s, %(hora_inicio)s, %(hora_fim)s,
                     %(foi_reserva)s, %(ch_usuario_inclusao)s)
                RETURNING id;
            """

            parms_oracle = {
                "estacao_id": parm_data["estacao_id"],
                "usuario_id": parm_data.get("usuario_id"),
                "data": parm_data["data"],
                "hora_inicio": parm_data["hora_inicio"],
                "hora_fim": parm_data["hora_fim"],
                "foi_reserva": parm_data["foi_reserva"],
                "ch_usuario_inclusao": parm_data.get("ch_usuario_inclusao", "SISTEMA")
            }

            new_id = self.execute_dml_command_parms(cmdSql, parms_oracle)

            return new_id

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)

    def update_log_ocupacao(self, parm_data: dict):

        try:
            rotina = 'update_log_ocupacao'
            cmdSql = """
                update log_ocupacao
                    set usuario_id = %(usuario_id)s,
                        hora_inicio = %(hora_inicio)s,
                        hora_fim = %(hora_fim)s,
                        foi_reserva = %(foi_reserva)s,
                        data_alteracao = CURRENT_TIMESTAMP,
                        ch_usuario_alteracao = %(ch_usuario_alteracao)s
                    where id = %(id)s
            """
            parms_oracle = {
                "id": parm_data["id"],
                "usuario_id": parm_data.get("usuario_id"),
                "hora_inicio": parm_data["hora_inicio"],
                "hora_fim": parm_data["hora_fim"],
                "foi_reserva": parm_data["foi_reserva"],
                "ch_usuario_alteracao": parm_data.get("ch_usuario_alteracao", "SISTEMA")
            }

            self.execute_dml_command_parms(cmdSql, parms_oracle)

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)

    def remove_log_ocupacao(self, id: int):

        try:
            rotina = 'remove_log_ocupacao'
            cmdSql = """
                delete from log_ocupacao
                where id = %(id)s
            """

            parms_oracle = {
                "id": id
            }

            self.execute_dml_command_parms(cmdSql, parms_oracle)

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)
