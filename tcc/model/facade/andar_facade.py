from tcc.util.util import convert_unique_dic_to_arrayDict

from ...util.exceptions import (
    FacadeException, NotFoundException,
    RequiredFieldException)
from ..dao.andar_dao import AndarDAO as andar_dao


class AndarFacade():

    def __init__(self):
        """construtor da classe AndarFacade"""
        self.andar_dao = andar_dao()

    # --------------------------------------------------------------------------
    # VALIDAÇÕES AUXILIARES
    # --------------------------------------------------------------------------
    def _validar_campos_criacao(self, parm_data: dict):
        """Valida os campos necessários para criar andar"""
        rotina = '_validar_campos_criacao'

        try:
            # Validar se biblioteca_id foi fornecido
            if not parm_data["biblioteca_id"]:
                raise RequiredFieldException(
                    "Campo 'biblioteca_id' é obrigatório")

            # Validar se numero foi fornecido
            if "numero" not in parm_data or parm_data["numero"] is None:
                raise RequiredFieldException(
                    "Campo 'numero' é obrigatório")

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def _validar_campos_atualizacao(self, parm_data: dict):
        """Valida os campos necessários para atualizar andar"""
        rotina = '_validar_campos_atualizacao'

        try:
            # Validar se ID foi fornecido
            if "id" not in parm_data or not parm_data["id"]:
                raise RequiredFieldException(
                    "Campo 'id' é obrigatório")

            # Validar se numero foi fornecido
            if "numero" not in parm_data or parm_data["numero"] is None:
                raise RequiredFieldException(
                    "Campo 'numero' é obrigatório")

            # Validar se registro existe no BD
            resultado = self.andar_dao.get_andar(id=parm_data["id"])
            if not resultado:
                raise NotFoundException(
                    f"Andar com ID {parm_data['id']} não encontrado")

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    # --------------------------------------------------------------------------
    # OPERAÇÕES CRUD
    # --------------------------------------------------------------------------

    def obter_andar(self, id: int = None):

        rotina = 'obter_andar'

        try:

            andar = convert_unique_dic_to_arrayDict(
                self.andar_dao.get_andar(id=id))

            return andar

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def criar_andar(self, parm_data: dict) -> int:
        rotina = 'criar_andar'

        try:

            # Validar campos
            self._validar_campos_criacao(parm_data)

            # eliminando espaços em branco laterais
            if "descricao" in parm_data and parm_data["descricao"]:
                parm_data["descricao"] = parm_data["descricao"].strip()

            id = self.andar_dao.add_andar(parm_data)
            self.andar_dao.database_commit()

            return id

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def apagar_andar(self, id: int):
        rotina = 'apagar_andar'

        try:

            resultado = self.andar_dao.get_andar(id=id)
            if not resultado:
                raise NotFoundException("Andar não encontrado")

            self.andar_dao.remove_andar(id)

            self.andar_dao.database_commit()

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def alterar_andar(self, parm_data: dict):
        rotina = 'alterar_andar'

        try:

            # Validar campos
            self._validar_campos_atualizacao(parm_data)

            # eliminando espaços em branco laterais
            if "descricao" in parm_data and parm_data["descricao"]:
                parm_data["descricao"] = parm_data["descricao"].strip()

            self.andar_dao.update_andar(parm_data)

            self.andar_dao.database_commit()

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)
