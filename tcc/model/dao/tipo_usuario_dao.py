import pandas as pd
from ...util.exceptions import DAOException
from ..base import tcc_dao_base as base


class TipoUsuarioDAO(base.DAOBase):

    def __init__(self):
        super().__init__()

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def get_tipo_usuario(self, id: int = None) -> dict:

        try:
            rotina = 'get_tipo_usuario'
            query = """
                select id, codigo, descricao,
                       data_inclusao, data_alteracao,
                       ch_usuario_inclusao, ch_usuario_alteracao
                from tipo_usuario
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

    def add_tipo_usuario(self, parm_data: dict) -> int:

        try:
            rotina = 'add_tipo_usuario'

            cmdSql = """
                INSERT INTO tipo_usuario
                    (codigo, descricao, ch_usuario_inclusao)
                VALUES
                    (%(codigo)s, %(descricao)s, %(ch_usuario_inclusao)s)
                RETURNING id;
            """

            parms_oracle = {
                "codigo": parm_data["codigo"],
                "descricao": parm_data["descricao"],
                "ch_usuario_inclusao": parm_data["ch_usuario_inclusao"]
            }

            new_id = self.execute_dml_command_parms(cmdSql, parms_oracle)

            return new_id

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)

    def update_tipo_usuario(self, parm_data: dict):

        try:
            rotina = 'update_tipo_usuario'
            cmdSql = """
                update tipo_usuario
                    set descricao = %(descricao)s,
                        data_alteracao = CURRENT_TIMESTAMP,
                        ch_usuario_alteracao = %(ch_usuario_alteracao)s
                    where id = %(id)s
            """
            parms_oracle = {
                "id": parm_data["id"],
                "descricao": parm_data["descricao"],
                "ch_usuario_alteracao": parm_data["ch_usuario_alteracao"]
            }

            self.execute_dml_command_parms(cmdSql, parms_oracle)

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)

    def remove_tipo_usuario(self, id: int):

        try:
            rotina = 'remove_tipo_usuario'
            cmdSql = """
                delete from tipo_usuario
                where id = %(id)s
            """

            parms_oracle = {
                "id": id
            }

            self.execute_dml_command_parms(cmdSql, parms_oracle)

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)
