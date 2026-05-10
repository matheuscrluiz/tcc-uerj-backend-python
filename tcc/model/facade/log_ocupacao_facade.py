from tcc.util.util import convert_unique_dic_to_arrayDict

from ...util.exceptions import (
    FacadeException, NotFoundException,
    RequiredFieldException, InvalidFieldException)
from ..dao.log_ocupacao_dao import LogOcupacaoDAO as log_ocupacao_dao


class LogOcupacaoFacade():

    def __init__(self):
        """construtor da classe LogOcupacaoFacade"""
        self.log_ocupacao_dao = log_ocupacao_dao()

    # --------------------------------------------------------------------------
    # VALIDAÇÕES AUXILIARES
    # --------------------------------------------------------------------------
    def _validar_campos_criacao(self, parm_data: dict):
        """Valida os campos necessários para criar log_ocupacao"""
        rotina = '_validar_campos_criacao'

        try:
            # Validar campos obrigatórios
            if "estacao_id" not in parm_data or not parm_data["estacao_id"]:
                raise RequiredFieldException(
                    "Campo 'estacao_id' é obrigatório")

            if "data" not in parm_data or not parm_data["data"]:
                raise RequiredFieldException(
                    "Campo 'data' é obrigatório")

            if "hora_inicio" not in parm_data or not parm_data["hora_inicio"]:
                raise RequiredFieldException(
                    "Campo 'hora_inicio' é obrigatório")

            if "hora_fim" not in parm_data or not parm_data["hora_fim"]:
                raise RequiredFieldException(
                    "Campo 'hora_fim' é obrigatório")

            if "foi_reserva" not in parm_data or not parm_data["foi_reserva"]:
                raise RequiredFieldException(
                    "Campo 'foi_reserva' é obrigatório")

            # Validar valores válidos de foi_reserva
            foi_reserva_valido = parm_data["foi_reserva"].upper()
            if foi_reserva_valido not in ['S', 'N']:
                raise InvalidFieldException(
                    "foi_reserva deve ser 'S' ou 'N'")

            # Validar que hora_inicio < hora_fim
            if parm_data["hora_inicio"] >= parm_data["hora_fim"]:
                raise InvalidFieldException(
                    "hora_inicio deve ser menor que hora_fim")

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def _validar_campos_atualizacao(self, parm_data: dict):
        """Valida os campos necessários para atualizar log_ocupacao"""
        rotina = '_validar_campos_atualizacao'

        try:
            # Validar se ID foi fornecido
            if "id" not in parm_data or not parm_data["id"]:
                raise RequiredFieldException(
                    "Campo 'id' é obrigatório")

            # Validar se hora_inicio foi fornecido
            if "hora_inicio" not in parm_data or not parm_data["hora_inicio"]:
                raise RequiredFieldException(
                    "Campo 'hora_inicio' é obrigatório")

            # Validar se hora_fim foi fornecido
            if "hora_fim" not in parm_data or not parm_data["hora_fim"]:
                raise RequiredFieldException(
                    "Campo 'hora_fim' é obrigatório")

            # Validar se foi_reserva foi fornecido
            if "foi_reserva" not in parm_data or not parm_data["foi_reserva"]:
                raise RequiredFieldException(
                    "Campo 'foi_reserva' é obrigatório")

            # Validar valores válidos de foi_reserva
            foi_reserva_valido = parm_data["foi_reserva"].upper()
            if foi_reserva_valido not in ['S', 'N']:
                raise InvalidFieldException(
                    "foi_reserva deve ser 'S' ou 'N'")

            # Validar que hora_inicio < hora_fim
            if parm_data["hora_inicio"] >= parm_data["hora_fim"]:
                raise InvalidFieldException(
                    "hora_inicio deve ser menor que hora_fim")

            # Validar se registro existe no BD
            resultado = self.log_ocupacao_dao.get_log_ocupacao(id=parm_data["id"])
            if not resultado:
                raise NotFoundException(
                    f"Log de ocupação com ID {parm_data['id']} não encontrado")

            # Validar que estacao_id e data não são alterados
            if parm_data.get('estacao_id') and parm_data['estacao_id'] != resultado[0]['estacao_id']:
                raise InvalidFieldException(
                    "estacao_id não pode ser atualizado"
                )

            if parm_data.get('data') and parm_data['data'] != resultado[0]['data']:
                raise InvalidFieldException(
                    "data não pode ser atualizada"
                )

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    # --------------------------------------------------------------------------
    # OPERAÇÕES CRUD
    # --------------------------------------------------------------------------

    def obter_log_ocupacao(self, id: int = None):

        rotina = 'obter_log_ocupacao'

        try:

            log_ocupacao = convert_unique_dic_to_arrayDict(
                self.log_ocupacao_dao.get_log_ocupacao(id=id))

            return log_ocupacao

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def criar_log_ocupacao(self, parm_data: dict) -> int:
        rotina = 'criar_log_ocupacao'

        try:

            # Validar campos
            self._validar_campos_criacao(parm_data)

            # converter foi_reserva para uppercase
            parm_data["foi_reserva"] = parm_data["foi_reserva"].strip().upper()

            id = self.log_ocupacao_dao.add_log_ocupacao(parm_data)
            self.log_ocupacao_dao.database_commit()

            return id

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def apagar_log_ocupacao(self, id: int):
        rotina = 'apagar_log_ocupacao'

        try:

            resultado = self.log_ocupacao_dao.get_log_ocupacao(id=id)
            if not resultado:
                raise NotFoundException("Log de ocupação não encontrado")

            self.log_ocupacao_dao.remove_log_ocupacao(id)

            self.log_ocupacao_dao.database_commit()

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def alterar_log_ocupacao(self, parm_data: dict):
        rotina = 'alterar_log_ocupacao'

        try:

            # Validar campos
            self._validar_campos_atualizacao(parm_data)

            # converter foi_reserva para uppercase
            parm_data["foi_reserva"] = parm_data["foi_reserva"].strip().upper()

            self.log_ocupacao_dao.update_log_ocupacao(parm_data)

            self.log_ocupacao_dao.database_commit()

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)
