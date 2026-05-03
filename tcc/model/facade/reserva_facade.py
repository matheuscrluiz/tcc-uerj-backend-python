from tcc.util.util import convert_unique_dic_to_arrayDict

from ...util.exceptions import (
    FacadeException, NotFoundException,
    RequiredFieldException, InvalidFieldException)
from ..dao.reserva_dao import ReservaDAO as reserva_dao


class ReservaFacade():

    def __init__(self):
        """construtor da classe ReservaFacade"""
        self.reserva_dao = reserva_dao()

    # --------------------------------------------------------------------------
    # VALIDAÇÕES AUXILIARES
    # --------------------------------------------------------------------------
    def _validar_campos_criacao(self, parm_data: dict):
        """Valida os campos necessários para criar reserva"""
        rotina = '_validar_campos_criacao'

        try:
            # Validar campos obrigatórios
            if "usuario_id" not in parm_data or not parm_data["usuario_id"]:
                raise RequiredFieldException(
                    "Campo 'usuario_id' é obrigatório")

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

            if "status" not in parm_data or not parm_data["status"]:
                raise RequiredFieldException(
                    "Campo 'status' é obrigatório")

            # Validar valores válidos de status
            status_valido = parm_data["status"].upper()
            if status_valido not in ['RESERVADA', 'CANCELADA',
                                     'EXPIRADA', 'FINALIZADA']:
                raise InvalidFieldException(
                    "Status deve ser 'RESERVADA', 'CANCELADA',"
                    " 'EXPIRADA' ou 'FINALIZADA'")

            # Validar que hora_inicio < hora_fim
            if parm_data["hora_inicio"] >= parm_data["hora_fim"]:
                raise InvalidFieldException(
                    "hora_inicio deve ser menor que hora_fim")

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def _validar_campos_atualizacao(self, parm_data: dict):
        """Valida os campos necessários para atualizar reserva"""
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

            # Validar se status foi fornecido
            if "status" not in parm_data or not parm_data["status"]:
                raise RequiredFieldException(
                    "Campo 'status' é obrigatório")

            # Validar valores válidos de status
            status_valido = parm_data["status"].upper()
            if status_valido not in ['RESERVADA', 'CANCELADA',
                                     'EXPIRADA', 'FINALIZADA']:
                raise InvalidFieldException(
                    "Status deve ser 'RESERVADA', 'CANCELADA',"
                    " 'EXPIRADA' ou 'FINALIZADA'")

            # Validar que hora_inicio < hora_fim
            if parm_data["hora_inicio"] >= parm_data["hora_fim"]:
                raise InvalidFieldException(
                    "hora_inicio deve ser menor que hora_fim")

            # Validar se registro existe no BD
            resultado = self.reserva_dao.get_reserva(id=parm_data["id"])
            if not resultado:
                raise NotFoundException(
                    f"Reserva com ID {parm_data['id']} não encontrada")

            # Validar que usuario_id, estacao_id e data não são alterados
            if parm_data['usuario_id'] != resultado[0]['usuario_id']:
                raise InvalidFieldException(
                    "usuario_id não pode ser atualizado"
                )

            if parm_data['estacao_id'] != resultado[0]['estacao_id']:
                raise InvalidFieldException(
                    "estacao_id não pode ser atualizado"
                )

            if parm_data['data'] != resultado[0]['data']:
                raise InvalidFieldException(
                    "data não pode ser atualizada"
                )

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    # --------------------------------------------------------------------------
    # OPERAÇÕES CRUD
    # --------------------------------------------------------------------------

    def obter_reserva(self, id: int = None):

        rotina = 'obter_reserva'

        try:

            reserva = convert_unique_dic_to_arrayDict(
                self.reserva_dao.get_reserva(id=id))

            return reserva

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def criar_reserva(self, parm_data: dict) -> int:
        rotina = 'criar_reserva'

        try:

            # Validar campos
            self._validar_campos_criacao(parm_data)

            # converter status para uppercase
            parm_data["status"] = parm_data["status"].strip().upper()

            id = self.reserva_dao.add_reserva(parm_data)
            self.reserva_dao.database_commit()

            return id

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def apagar_reserva(self, id: int):
        rotina = 'apagar_reserva'

        try:

            resultado = self.reserva_dao.get_reserva(id=id)
            if not resultado:
                raise NotFoundException("Reserva não encontrada")

            self.reserva_dao.remove_reserva(id)

            self.reserva_dao.database_commit()

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def alterar_reserva(self, parm_data: dict):
        rotina = 'alterar_reserva'

        try:

            # Validar campos
            self._validar_campos_atualizacao(parm_data)

            # converter status para uppercase
            parm_data["status"] = parm_data["status"].strip().upper()

            self.reserva_dao.update_reserva(parm_data)

            self.reserva_dao.database_commit()

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)
