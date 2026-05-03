from tcc.util.util import convert_unique_dic_to_arrayDict

from ...util.exceptions import (
    FacadeException, NotFoundException,
    RequiredFieldException, InvalidFieldException)
from ..dao.tipo_estacao_dao import TipoEstacaoDAO as tipo_estacao_dao


class TipoEstacaoFacade():

    def __init__(self):
        """construtor da classe TipoEstacaoFacade"""
        self.tipo_estacao_dao = tipo_estacao_dao()

    # --------------------------------------------------------------------------
    # VALIDAÇÕES AUXILIARES
    # --------------------------------------------------------------------------
    def _validar_campos_criacao(self, parm_data: dict):
        """Valida os campos necessários para criar tipo_estacao"""
        rotina = '_validar_campos_criacao'

        try:
            codigo = parm_data.get("codigo", "").strip()

            # Validar se código foi fornecido e não é vazio
            if "codigo" not in parm_data or not parm_data["codigo"]:
                raise RequiredFieldException(
                    "Campo 'codigo' é obrigatório")

            # Validar se descrição foi fornecida e não é vazia
            if "descricao" not in parm_data or not parm_data["descricao"]:
                raise RequiredFieldException(
                    "Campo 'descricao' é obrigatório")

            # Validar se permite_reserva foi fornecido
            if not parm_data["permite_reserva"]:
                raise RequiredFieldException(
                    "Campo 'permite_reserva' é obrigatório")

            # Validar se código já existe (UNIQUE)
            resultado = self.tipo_estacao_dao.get_tipo_estacao()
            if resultado:
                for item in resultado:
                    if item.get("codigo") == codigo:
                        raise InvalidFieldException(
                            f"Tipo de estação com código '{codigo}' já existe")

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def _validar_campos_atualizacao(self, parm_data: dict):
        """Valida os campos necessários para atualizar tipo_estacao"""
        rotina = '_validar_campos_atualizacao'

        try:
            # Validar se ID foi fornecido
            if "id" not in parm_data or not parm_data["id"]:
                raise RequiredFieldException(
                    "Campo 'id' é obrigatório")

            # Validar se descrição foi fornecida e não é vazia
            if "descricao" not in parm_data or not parm_data["descricao"]:
                raise RequiredFieldException(
                    "Campo 'descricao' é obrigatório")

            # Validar se permite_reserva foi fornecido
            if not parm_data["permite_reserva"]:
                raise RequiredFieldException(
                    "Campo 'permite_reserva' é obrigatório")

            # Validar se registro existe no BD
            resultado = self.tipo_estacao_dao.get_tipo_estacao(
                id=parm_data["id"])
            if not resultado:
                raise NotFoundException(
                    f"Tipo de estação com ID {parm_data['id']} não encontrado")

            # Informar que código não pode ser alterado
            if parm_data['codigo'] != resultado[0]['codigo']:
                raise InvalidFieldException(
                    "Código não pode ser atualizado"
                )

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    # --------------------------------------------------------------------------
    # OPERAÇÕES CRUD
    # --------------------------------------------------------------------------

    def obter_tipo_estacao(self, id: int = None):

        rotina = 'obter_tipo_estacao'

        try:

            tipo_estacao = convert_unique_dic_to_arrayDict(
                self.tipo_estacao_dao.get_tipo_estacao(id=id))

            return tipo_estacao

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def criar_tipo_estacao(self, parm_data: dict) -> int:
        rotina = 'criar_tipo_estacao'

        try:

            # Validar campos
            self._validar_campos_criacao(parm_data)

            # eliminando espaços em branco laterais
            parm_data["codigo"] = parm_data["codigo"].strip()
            parm_data["descricao"] = parm_data["descricao"].strip()

            id = self.tipo_estacao_dao.add_tipo_estacao(parm_data)
            self.tipo_estacao_dao.database_commit()

            return id

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def apagar_tipo_estacao(self, id: int):
        rotina = 'apagar_tipo_estacao'

        try:

            resultado = self.tipo_estacao_dao.get_tipo_estacao(
                id=id)
            if not resultado:
                raise NotFoundException("Tipo de estação não encontrado")

            self.tipo_estacao_dao.remove_tipo_estacao(id)

            self.tipo_estacao_dao.database_commit()

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def alterar_tipo_estacao(self, parm_data: dict):
        rotina = 'alterar_tipo_estacao'

        try:

            # Validar campos
            self._validar_campos_atualizacao(parm_data)

            # eliminando espaços em branco laterais
            parm_data["descricao"] = parm_data["descricao"].strip()

            self.tipo_estacao_dao.update_tipo_estacao(parm_data)

            self.tipo_estacao_dao.database_commit()

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)
