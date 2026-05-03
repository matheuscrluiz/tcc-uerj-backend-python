import pandas as pd
from ...util.exceptions import DAOException
from ..base import tcc_dao_base as base


class BibliotecaDAO(base.DAOBase):

    def __init__(self):
        super().__init__()

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def get_biblioteca(self, id: int = None) -> dict:

        try:
            rotina = 'get_biblioteca'
            query = """
                select id, nome, descricao,
                       data_inclusao, data_alteracao,
                       ch_usuario_inclusao, ch_usuario_alteracao
                from biblioteca
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

    def add_biblioteca(self, parm_data: dict) -> int:

        try:
            rotina = 'add_biblioteca'

            cmdSql = """
                INSERT INTO biblioteca
                    (nome, descricao, ch_usuario_inclusao)
                VALUES
                    (%(nome)s, %(descricao)s, %(ch_usuario_inclusao)s)
                RETURNING id;
            """

            parms_oracle = {
                "nome": parm_data["nome"],
                "descricao": parm_data.get("descricao", ""),
                "ch_usuario_inclusao": parm_data["ch_usuario_inclusao"]
            }

            new_id = self.execute_dml_command_parms(cmdSql, parms_oracle)

            return new_id

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)

    def update_biblioteca(self, parm_data: dict):

        try:
            rotina = 'update_biblioteca'
            cmdSql = """
                update biblioteca
                    set nome = %(nome)s,
                        descricao = %(descricao)s,
                        data_alteracao = CURRENT_TIMESTAMP,
                        ch_usuario_alteracao = %(ch_usuario_alteracao)s
                    where id = %(id)s
            """
            parms_oracle = {
                "id": parm_data["id"],
                "nome": parm_data["nome"],
                "descricao": parm_data.get("descricao", ""),
                "ch_usuario_alteracao": parm_data["ch_usuario_alteracao"]
            }

            self.execute_dml_command_parms(cmdSql, parms_oracle)

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)

    def remove_biblioteca(self, id: int):

        try:
            rotina = 'remove_biblioteca'
            cmdSql = """
                delete from biblioteca
                where id = %(id)s
            """

            parms_oracle = {
                "id": id
            }

            self.execute_dml_command_parms(cmdSql, parms_oracle)

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)
