from tcc.util.util import convert_unique_dic_to_arrayDict

from ...util.exceptions import (
    FacadeException, NotFoundException,
    RequiredFieldException, InvalidFieldException)
from ..dao.estacao_dao import EstacaoDAO as estacao_dao


class EstacaoFacade():

    def __init__(self):
        """construtor da classe EstacaoFacade"""
        self.estacao_dao = estacao_dao()

    # --------------------------------------------------------------------------
    # VALIDAÇÕES AUXILIARES
    # --------------------------------------------------------------------------
    def _validar_campos_criacao(self, parm_data: dict):
        """Valida os campos necessários para criar estacao"""
        rotina = '_validar_campos_criacao'

        try:
            # Validar campos obrigatórios
            if "andar_id" not in parm_data or not parm_data["andar_id"]:
                raise RequiredFieldException(
                    "Campo 'andar_id' é obrigatório")

            if not parm_data["tipo_estacao_id"]:
                raise RequiredFieldException(
                    "Campo 'tipo_estacao_id' é obrigatório")

            if "codigo" not in parm_data or not parm_data["codigo"]:
                raise RequiredFieldException(
                    "Campo 'codigo' é obrigatório")

            if "status" not in parm_data or not parm_data["status"]:
                raise RequiredFieldException(
                    "Campo 'status' é obrigatório")

            # Validar valores válidos de status
            status_valido = parm_data["status"].upper()
            if status_valido not in ['ATIVA', 'MANUTENCAO']:
                raise InvalidFieldException(
                    "Status deve ser 'ATIVA' ou 'MANUTENCAO'")

            # Validar unicidade de (andar_id, codigo)
            resultado = self.estacao_dao.get_estacao()
            if resultado:
                for item in resultado:
                    if (item.get("andar_id") == parm_data["andar_id"] and
                            item.get("codigo") == parm_data["codigo"]):
                        raise InvalidFieldException(
                            f"Estação com código '{parm_data['codigo']}'"
                            "já existe neste andar")

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def _validar_campos_atualizacao(self, parm_data: dict):
        """Valida os campos necessários para atualizar estacao"""
        rotina = '_validar_campos_atualizacao'

        try:
            # Validar se ID foi fornecido
            if "id" not in parm_data or not parm_data["id"]:
                raise RequiredFieldException(
                    "Campo 'id' é obrigatório")

            # Validar se tipo_estacao_id foi fornecido
            if not parm_data["tipo_estacao_id"]:
                raise RequiredFieldException(
                    "Campo 'tipo_estacao_id' é obrigatório")

            # Validar se status foi fornecido
            if "status" not in parm_data or not parm_data["status"]:
                raise RequiredFieldException(
                    "Campo 'status' é obrigatório")

            # Validar valores válidos de status
            status_valido = parm_data["status"].upper()
            if status_valido not in ['ATIVA', 'MANUTENCAO']:
                raise InvalidFieldException(
                    "Status deve ser 'ATIVA' ou 'MANUTENCAO'")

            # Validar se registro existe no BD
            resultado = self.estacao_dao.get_estacao(id=parm_data["id"])
            if not resultado:
                raise NotFoundException(
                    f"Estação com ID {parm_data['id']} não encontrada")

            # Validar que andar_id e codigo não são alterados (UNIQUE)
            if parm_data['andar_id'] != resultado[0]['andar_id']:
                raise InvalidFieldException(
                    "andar_id não pode ser atualizado"
                )

            if parm_data['codigo'] != resultado[0]['codigo']:
                raise InvalidFieldException(
                    "codigo não pode ser atualizado"
                )

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    # --------------------------------------------------------------------------
    # OPERAÇÕES CRUD
    # --------------------------------------------------------------------------

    def obter_estacao(self, id: int = None):

        rotina = 'obter_estacao'

        try:

            estacao = convert_unique_dic_to_arrayDict(
                self.estacao_dao.get_estacao(id=id))

            return estacao

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def criar_estacao(self, parm_data: dict) -> int:
        rotina = 'criar_estacao'

        try:

            # Validar campos
            self._validar_campos_criacao(parm_data)

            # eliminando espaços em branco laterais
            parm_data["codigo"] = parm_data["codigo"].strip()
            parm_data["status"] = parm_data["status"].strip().upper()

            id = self.estacao_dao.add_estacao(parm_data)
            self.estacao_dao.database_commit()

            return id

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def apagar_estacao(self, id: int):
        rotina = 'apagar_estacao'

        try:

            resultado = self.estacao_dao.get_estacao(id=id)
            if not resultado:
                raise NotFoundException("Estação não encontrada")

            self.estacao_dao.remove_estacao(id)

            self.estacao_dao.database_commit()

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def alterar_estacao(self, parm_data: dict):
        rotina = 'alterar_estacao'

        try:

            # Validar campos
            self._validar_campos_atualizacao(parm_data)

            # eliminando espaços em branco laterais
            parm_data["status"] = parm_data["status"].strip().upper()

            self.estacao_dao.update_estacao(parm_data)

            self.estacao_dao.database_commit()

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)
