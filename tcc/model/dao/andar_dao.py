import pandas as pd
from ...util.exceptions import DAOException
from ..base import tcc_dao_base as base


class AndarDAO(base.DAOBase):

    def __init__(self):
        super().__init__()

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def get_andar(self, id: int = None) -> dict:

        try:
            rotina = 'get_andar'
            query = """
                select id, biblioteca_id, numero, descricao,
                       data_inclusao, data_alteracao,
                       ch_usuario_inclusao, ch_usuario_alteracao
                from andar
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

    def add_andar(self, parm_data: dict) -> int:

        try:
            rotina = 'add_andar'

            cmdSql = """
                INSERT INTO andar
                    (biblioteca_id, numero, descricao, ch_usuario_inclusao)
                VALUES
                    (%(biblioteca_id)s, %(numero)s, %(descricao)s,
                      %(ch_usuario_inclusao)s)
                RETURNING id;
            """

            parms_oracle = {
                "biblioteca_id": parm_data["biblioteca_id"],
                "numero": parm_data["numero"],
                "descricao": parm_data.get("descricao", ""),
                "ch_usuario_inclusao": parm_data["ch_usuario_inclusao"]
            }

            new_id = self.execute_dml_command_parms(cmdSql, parms_oracle)

            return new_id

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)

    def update_andar(self, parm_data: dict):

        try:
            rotina = 'update_andar'
            cmdSql = """
                update andar
                    set numero = %(numero)s,
                        descricao = %(descricao)s,
                        data_alteracao = CURRENT_TIMESTAMP,
                        ch_usuario_alteracao = %(ch_usuario_alteracao)s
                    where id = %(id)s
            """
            parms_oracle = {
                "id": parm_data["id"],
                "numero": parm_data["numero"],
                "descricao": parm_data.get("descricao", ""),
                "ch_usuario_alteracao": parm_data["ch_usuario_alteracao"]
            }

            self.execute_dml_command_parms(cmdSql, parms_oracle)

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)

    def remove_andar(self, id: int):

        try:
            rotina = 'remove_andar'
            cmdSql = """
                delete from andar
                where id = %(id)s
            """

            parms_oracle = {
                "id": id
            }

            self.execute_dml_command_parms(cmdSql, parms_oracle)

        except DAOException as erro:
            raise DAOException(__file__, rotina, erro)
