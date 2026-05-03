from tcc.util.util import convert_unique_dic_to_arrayDict

from ...util.exceptions import (
    FacadeException, NotFoundException,
    RequiredFieldException, InvalidFieldException)
from ..dao.usuario_dao import UsuarioDAO as usuario_dao


class UsuarioFacade():

    def __init__(self):
        """construtor da classe UsuarioFacade"""
        self.usuario_dao = usuario_dao()

    # --------------------------------------------------------------------------
    # VALIDAÇÕES AUXILIARES
    # --------------------------------------------------------------------------
    def _validar_campos_criacao(self, parm_data: dict):
        """Valida os campos necessários para criar usuario"""
        rotina = '_validar_campos_criacao'

        try:
            # Validar campos obrigatórios
            if "ch_rede" not in parm_data or not parm_data["ch_rede"]:
                raise RequiredFieldException(
                    "Campo 'ch_rede' é obrigatório")

            if "nome" not in parm_data or not parm_data["nome"]:
                raise RequiredFieldException(
                    "Campo 'nome' é obrigatório")

            if "email" not in parm_data or not parm_data["email"]:
                raise RequiredFieldException(
                    "Campo 'email' é obrigatório")

            if "matricula" not in parm_data or not parm_data["matricula"]:
                raise RequiredFieldException(
                    "Campo 'matricula' é obrigatório")

            if "senha_hash" not in parm_data or not parm_data["senha_hash"]:
                raise RequiredFieldException(
                    "Campo 'senha_hash' é obrigatório")

            if not parm_data["tipo_usuario_id"]:
                raise RequiredFieldException(
                    "Campo 'tipo_usuario_id' é obrigatório")

            # Validar unicidade de campos
            resultado = self.usuario_dao.get_usuario()
            if resultado:
                for item in resultado:
                    if item.get("ch_rede") == parm_data["ch_rede"]:
                        raise InvalidFieldException("Usuário já existe")
                    if item.get("email") == parm_data["email"]:
                        raise InvalidFieldException("Email já existe")
                    if item.get("matricula") == parm_data["matricula"]:
                        raise InvalidFieldException("Matricula já existe")

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def _validar_campos_atualizacao(self, parm_data: dict):
        """Valida os campos necessários para atualizar usuario"""
        rotina = '_validar_campos_atualizacao'

        try:
            # Validar se ID foi fornecido
            if "id" not in parm_data or not parm_data["id"]:
                raise RequiredFieldException(
                    "Campo 'id' é obrigatório")

            # Validar campos obrigatórios
            if "nome" not in parm_data or not parm_data["nome"]:
                raise RequiredFieldException(
                    "Campo 'nome' é obrigatório")

            if "email" not in parm_data or not parm_data["email"]:
                raise RequiredFieldException(
                    "Campo 'email' é obrigatório")

            if not parm_data["tipo_usuario_id"]:
                raise RequiredFieldException(
                    "Campo 'tipo_usuario_id' é obrigatório")

            # Validar se registro existe no BD
            resultado = self.usuario_dao.get_usuario(id=parm_data["id"])
            if not resultado:
                raise NotFoundException(
                    f"Usuário com ID {parm_data['id']} não encontrado")

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    # --------------------------------------------------------------------------
    # OPERAÇÕES CRUD
    # --------------------------------------------------------------------------

    def obter_usuario(self, id: int = None):

        rotina = 'obter_usuario'

        try:

            usuario = convert_unique_dic_to_arrayDict(
                self.usuario_dao.get_usuario(id=id))

            return usuario

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def criar_usuario(self, parm_data: dict) -> int:
        rotina = 'criar_usuario'

        try:

            # Validar campos
            self._validar_campos_criacao(parm_data)

            # eliminando espaços em branco laterais
            parm_data["ch_rede"] = parm_data["ch_rede"].strip()
            parm_data["nome"] = parm_data["nome"].strip()
            parm_data["email"] = parm_data["email"].strip()
            parm_data["matricula"] = parm_data["matricula"].strip()

            id = self.usuario_dao.add_usuario(parm_data)
            self.usuario_dao.database_commit()

            return id

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def apagar_usuario(self, id: int):
        rotina = 'apagar_usuario'

        try:

            resultado = self.usuario_dao.get_usuario(id=id)
            if not resultado:
                raise NotFoundException("Usuário não encontrado")

            self.usuario_dao.remove_usuario(id)

            self.usuario_dao.database_commit()

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def alterar_usuario(self, parm_data: dict):
        rotina = 'alterar_usuario'

        try:

            # Validar campos
            self._validar_campos_atualizacao(parm_data)

            # eliminando espaços em branco laterais
            parm_data["nome"] = parm_data["nome"].strip()
            parm_data["email"] = parm_data["email"].strip()

            self.usuario_dao.update_usuario(parm_data)

            self.usuario_dao.database_commit()

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)
