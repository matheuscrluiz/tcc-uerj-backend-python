from tcc.util.util import convert_unique_dic_to_arrayDict

from ...util.exceptions import (
    FacadeException, NotFoundException,
    RequiredFieldException)
from ..dao.biblioteca_dao import BibliotecaDAO as biblioteca_dao


class BibliotecaFacade():

    def __init__(self):
        """construtor da classe BibliotecaFacade"""
        self.biblioteca_dao = biblioteca_dao()

    # --------------------------------------------------------------------------
    # VALIDAÇÕES AUXILIARES
    # --------------------------------------------------------------------------
    def _validar_campos_criacao(self, parm_data: dict):
        """Valida os campos necessários para criar biblioteca"""
        rotina = '_validar_campos_criacao'

        try:
            # Validar se nome foi fornecido e não é vazio
            if "nome" not in parm_data or not parm_data["nome"]:
                raise RequiredFieldException(
                    "Campo 'nome' é obrigatório")

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def _validar_campos_atualizacao(self, parm_data: dict):
        """Valida os campos necessários para atualizar biblioteca"""
        rotina = '_validar_campos_atualizacao'

        try:
            # Validar se ID foi fornecido
            if "id" not in parm_data or not parm_data["id"]:
                raise RequiredFieldException(
                    "Campo 'id' é obrigatório")

            # Validar se nome foi fornecido e não é vazio
            if "nome" not in parm_data or not parm_data["nome"]:
                raise RequiredFieldException(
                    "Campo 'nome' é obrigatório")

            # Validar se registro existe no BD
            resultado = self.biblioteca_dao.get_biblioteca(
                id=parm_data["id"])
            if not resultado:
                raise NotFoundException(
                    f"Biblioteca com ID {parm_data['id']} não encontrada")

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    # --------------------------------------------------------------------------
    # OPERAÇÕES CRUD
    # --------------------------------------------------------------------------

    def obter_biblioteca(self, id: int = None):

        rotina = 'obter_biblioteca'

        try:

            biblioteca = convert_unique_dic_to_arrayDict(
                self.biblioteca_dao.get_biblioteca(id=id))

            return biblioteca

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def criar_biblioteca(self, parm_data: dict) -> int:
        rotina = 'criar_biblioteca'

        try:

            # Validar campos
            self._validar_campos_criacao(parm_data)

            # eliminando espaços em branco laterais
            parm_data["nome"] = parm_data["nome"].strip()
            if "descricao" in parm_data:
                parm_data["descricao"] = parm_data["descricao"].strip()

            id = self.biblioteca_dao.add_biblioteca(parm_data)
            self.biblioteca_dao.database_commit()

            return id

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def apagar_biblioteca(self, id: int):
        rotina = 'apagar_biblioteca'

        try:

            resultado = self.biblioteca_dao.get_biblioteca(id=id)
            if not resultado:
                raise NotFoundException("Biblioteca não encontrada")

            self.biblioteca_dao.remove_biblioteca(id)

            self.biblioteca_dao.database_commit()

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def alterar_biblioteca(self, parm_data: dict):
        rotina = 'alterar_biblioteca'

        try:

            # Validar campos
            self._validar_campos_atualizacao(parm_data)

            # eliminando espaços em branco laterais
            parm_data["nome"] = parm_data["nome"].strip()
            if "descricao" in parm_data:
                parm_data["descricao"] = parm_data["descricao"].strip()

            self.biblioteca_dao.update_biblioteca(parm_data)

            self.biblioteca_dao.database_commit()

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)
