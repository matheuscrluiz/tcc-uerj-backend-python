import pandas as pd
from ...util.exceptions import DAOException
from ..base import tcc_dao_base as base


class UsuarioDAO(base.DAOBase):

    def __init__(self):
        super().__init__()

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def get_usuario(self, id: int = None) -> dict:

        try:
            rotina = 'get_usuario'
            query = """
                select id, ch_rede, nome, email, matricula, senha_hash,
                       tipo_usuario_id, ativo,
                       data_inclusao, data_alteracao,
                       ch_usuario_inclusao, ch_usuario_alteracao
                from usuario
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

    def add_usuario(self, parm_data: dict) -> int:

        try:
            rotina = 'add_usuario'

            cmdSql = """
                INSERT INTO usuario
                    (ch_rede, nome, email, matricula, senha_hash,
                     tipo_usuario_id, ativo, ch_usuario_inclusao)
                VALUES
                    (%(ch_rede)s, %(nome)s, %(email)s, %(matricula)s,
                    %(senha_hash)s, %(tipo_usuario_id)s,
                      %(ativo)s, %(ch_usuario_inclusao)s)
                RETURNING id;
            """

            parms_oracle = {
                "ch_rede": parm_data["ch_rede"],
                "nome": parm_data["nome"],
                "email": parm_data["email"],
                "matricula": parm_data["matricula"],
                "senha_hash": parm_data["senha_hash"],
                "tipo_usuario_id": parm_data["tipo_usuario_id"],
                "ativo": parm_data.get("ativo", True),
                "ch_usuario_inclusao": parm_data["ch_usuario_inclusao"]
            }

            new_id = self.execute_dml_command_parms(cmdSql, parms_oracle)

            return new_id

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)

    def update_usuario(self, parm_data: dict):

        try:
            rotina = 'update_usuario'
            cmdSql = """
                update usuario
                    set nome = %(nome)s,
                        email = %(email)s,
                        tipo_usuario_id = %(tipo_usuario_id)s,
                        ativo = %(ativo)s,
                        data_alteracao = CURRENT_TIMESTAMP,
                        ch_usuario_alteracao = %(ch_usuario_alteracao)s
                    where id = %(id)s
            """
            parms_oracle = {
                "id": parm_data["id"],
                "nome": parm_data["nome"],
                "email": parm_data["email"],
                "tipo_usuario_id": parm_data["tipo_usuario_id"],
                "ativo": parm_data.get("ativo", True),
                "ch_usuario_alteracao": parm_data["ch_usuario_alteracao"]
            }

            self.execute_dml_command_parms(cmdSql, parms_oracle)

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)

    def remove_usuario(self, id: int):

        try:
            rotina = 'remove_usuario'
            cmdSql = """
                delete from usuario
                where id = %(id)s
            """

            parms_oracle = {
                "id": id
            }

            self.execute_dml_command_parms(cmdSql, parms_oracle)

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)
