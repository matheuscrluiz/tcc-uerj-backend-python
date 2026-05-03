# coding: utf-8
from flask import jsonify, request
from flask_restx import Resource
from flask_restx.namespace import Namespace

from tcc.util.util import get_dict_retorno_endpoint
from tcc.view.api.model.model_reserva import generate_reserva_model
from ...util.constants import MSG_SUCESSO, TIP_RETORNO_SUCESS
from ...model.facade.reserva_facade import (
    ReservaFacade as reserva_f)
# ---------------------------->>
# NameSpace
# ---------------------------->>

api = Namespace('reserva', description='reserva')

# ---------------------------->>
# Model
# ---------------------------->>


post_reserva_model = generate_reserva_model(api, "post")
put_reserva_model = generate_reserva_model(api, "put")

model_get_reserva = api.parser().add_argument(
    name='id',
    type=int,
    required=False
)
model_delete_reserva = api.parser().add_argument(
    name='id',
    type=int,
    required=True
)

# ---------------------------->>
# Rotas
# ---------------------------->>


@api.route('')
class ResourceReserva(Resource):

    @api.expect(model_get_reserva, validate=True)
    def get(self):
        id_param = request.args.get('id')
        result = reserva_f().obter_reserva(id=id_param)

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS, MSG_SUCESSO, result)
        )

    @api.expect(post_reserva_model, validate=True)
    def post(self):

        result = reserva_f().criar_reserva(request.get_json())

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS, MSG_SUCESSO, result)
        )

    @api.expect(put_reserva_model, validate=True)
    def put(self):

        reserva_f().alterar_reserva(request.get_json())

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS,  MSG_SUCESSO, None)
        )

    @api.expect(model_delete_reserva, validate=True)
    def delete(self):
        id_param = request.args.get('id')
        reserva_f().apagar_reserva(id=id_param)

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS,  MSG_SUCESSO, None)
        )
