import pandas as pd
from ...util.exceptions import DAOException
from ..base import tcc_dao_base as base


class EstacaoDAO(base.DAOBase):

    def __init__(self):
        super().__init__()

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def get_estacao(self, id: int = None) -> dict:

        try:
            rotina = 'get_estacao'
            query = """
                select id, andar_id, tipo_estacao_id, codigo, capacidade,
                    status, data_inclusao, data_alteracao,
                       ch_usuario_inclusao, ch_usuario_alteracao
                from estacao
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

    def add_estacao(self, parm_data: dict) -> int:

        try:
            rotina = 'add_estacao'

            cmdSql = """
                INSERT INTO estacao
                    (andar_id, tipo_estacao_id, codigo, capacidade, status,
                      ch_usuario_inclusao)
                VALUES
                    (%(andar_id)s, %(tipo_estacao_id)s, %(codigo)s,
                      %(capacidade)s, %(status)s, %(ch_usuario_inclusao)s)
                RETURNING id;
            """

            parms_oracle = {
                "andar_id": parm_data["andar_id"],
                "tipo_estacao_id": parm_data["tipo_estacao_id"],
                "codigo": parm_data["codigo"],
                "capacidade": parm_data.get("capacidade"),
                "status": parm_data["status"],
                "ch_usuario_inclusao": parm_data["ch_usuario_inclusao"]
            }

            new_id = self.execute_dml_command_parms(cmdSql, parms_oracle)

            return new_id

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)

    def update_estacao(self, parm_data: dict):

        try:
            rotina = 'update_estacao'
            cmdSql = """
                update estacao
                    set tipo_estacao_id = %(tipo_estacao_id)s,
                        capacidade = %(capacidade)s,
                        status = %(status)s,
                        data_alteracao = CURRENT_TIMESTAMP,
                        ch_usuario_alteracao = %(ch_usuario_alteracao)s
                    where id = %(id)s
            """
            parms_oracle = {
                "id": parm_data["id"],
                "tipo_estacao_id": parm_data["tipo_estacao_id"],
                "capacidade": parm_data.get("capacidade"),
                "status": parm_data["status"],
                "ch_usuario_alteracao": parm_data["ch_usuario_alteracao"]
            }

            self.execute_dml_command_parms(cmdSql, parms_oracle)

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)

    def remove_estacao(self, id: int):

        try:
            rotina = 'remove_estacao'
            cmdSql = """
                delete from estacao
                where id = %(id)s
            """

            parms_oracle = {
                "id": id
            }

            self.execute_dml_command_parms(cmdSql, parms_oracle)

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)
