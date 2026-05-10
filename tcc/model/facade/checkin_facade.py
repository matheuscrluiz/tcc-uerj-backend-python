from tcc.util.util import convert_unique_dic_to_arrayDict

from ...util.exceptions import (
    FacadeException, NotFoundException,
    RequiredFieldException, InvalidFieldException)
from ..dao.checkin_dao import CheckinDAO as checkin_dao


class CheckinFacade():

    def __init__(self):
        """construtor da classe CheckinFacade"""
        self.checkin_dao = checkin_dao()

    # --------------------------------------------------------------------------
    # VALIDAÇÕES AUXILIARES
    # --------------------------------------------------------------------------
    def _validar_campos_criacao(self, parm_data: dict):
        """Valida os campos necessários para criar checkin"""
        rotina = '_validar_campos_criacao'

        try:
            # Validar campos obrigatórios
            if "reserva_id" not in parm_data or not parm_data["reserva_id"]:
                raise RequiredFieldException(
                    "Campo 'reserva_id' é obrigatório")

            if "status" not in parm_data or not parm_data["status"]:
                raise RequiredFieldException(
                    "Campo 'status' é obrigatório")

            # Validar valores válidos de status
            status_valido = parm_data["status"].upper()
            if status_valido not in ['PRESENTE', 'NO_SHOW']:
                raise InvalidFieldException(
                    "Status deve ser 'PRESENTE' ou 'NO_SHOW'")

            # Validar unicidade de reserva_id
            resultado = self.checkin_dao.get_checkin()
            if resultado:
                for item in resultado:
                    if item.get("reserva_id") == parm_data["reserva_id"]:
                        raise InvalidFieldException(
                            f"Já existe um check-in para esta reserva")

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def _validar_campos_atualizacao(self, parm_data: dict):
        """Valida os campos necessários para atualizar checkin"""
        rotina = '_validar_campos_atualizacao'

        try:
            # Validar se ID foi fornecido
            if "id" not in parm_data or not parm_data["id"]:
                raise RequiredFieldException(
                    "Campo 'id' é obrigatório")

            # Validar se status foi fornecido
            if "status" not in parm_data or not parm_data["status"]:
                raise RequiredFieldException(
                    "Campo 'status' é obrigatório")

            # Validar valores válidos de status
            status_valido = parm_data["status"].upper()
            if status_valido not in ['PRESENTE', 'NO_SHOW']:
                raise InvalidFieldException(
                    "Status deve ser 'PRESENTE' ou 'NO_SHOW'")

            # Validar se registro existe no BD
            resultado = self.checkin_dao.get_checkin(id=parm_data["id"])
            if not resultado:
                raise NotFoundException(
                    f"Check-in com ID {parm_data['id']} não encontrado")

            # Validar que reserva_id não é alterado (UNIQUE)
            if parm_data.get('reserva_id') and parm_data['reserva_id'] != resultado[0]['reserva_id']:
                raise InvalidFieldException(
                    "reserva_id não pode ser atualizado"
                )

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    # --------------------------------------------------------------------------
    # OPERAÇÕES CRUD
    # --------------------------------------------------------------------------

    def obter_checkin(self, id: int = None):

        rotina = 'obter_checkin'

        try:

            checkin = convert_unique_dic_to_arrayDict(
                self.checkin_dao.get_checkin(id=id))

            return checkin

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def criar_checkin(self, parm_data: dict) -> int:
        rotina = 'criar_checkin'

        try:

            # Validar campos
            self._validar_campos_criacao(parm_data)

            # converter status para uppercase
            parm_data["status"] = parm_data["status"].strip().upper()

            id = self.checkin_dao.add_checkin(parm_data)
            self.checkin_dao.database_commit()

            return id

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def apagar_checkin(self, id: int):
        rotina = 'apagar_checkin'

        try:

            resultado = self.checkin_dao.get_checkin(id=id)
            if not resultado:
                raise NotFoundException("Check-in não encontrado")

            self.checkin_dao.remove_checkin(id)

            self.checkin_dao.database_commit()

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)

    def alterar_checkin(self, parm_data: dict):
        rotina = 'alterar_checkin'

        try:

            # Validar campos
            self._validar_campos_atualizacao(parm_data)

            # converter status para uppercase
            parm_data["status"] = parm_data["status"].strip().upper()

            self.checkin_dao.update_checkin(parm_data)

            self.checkin_dao.database_commit()

        except Exception as erro:
            raise FacadeException(__file__, rotina, erro)
