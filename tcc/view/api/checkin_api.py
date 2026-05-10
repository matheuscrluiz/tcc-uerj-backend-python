# coding: utf-8
from flask import jsonify, request
from flask_restx import Resource
from flask_restx.namespace import Namespace

from tcc.util.util import get_dict_retorno_endpoint
from tcc.view.api.model.model_checkin import generate_checkin_model
from ...util.constants import MSG_SUCESSO, TIP_RETORNO_SUCESS
from ...model.facade.checkin_facade import (
    CheckinFacade as checkin_f)
# ---------------------------->>
# NameSpace
# ---------------------------->>

api = Namespace('checkin', description='checkin')

# ---------------------------->>
# Model
# ---------------------------->>


post_checkin_model = generate_checkin_model(api, "post")
put_checkin_model = generate_checkin_model(api, "put")

model_get_checkin = api.parser().add_argument(
    name='id',
    type=int,
    required=False
)
model_delete_checkin = api.parser().add_argument(
    name='id',
    type=int,
    required=True
)

# ---------------------------->>
# Rotas
# ---------------------------->>


@api.route('')
class ResourceCheckin(Resource):

    @api.expect(model_get_checkin, validate=True)
    def get(self):
        id_param = request.args.get('id')
        result = checkin_f().obter_checkin(id=id_param)

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS, MSG_SUCESSO, result)
        )

    @api.expect(post_checkin_model, validate=True)
    def post(self):

        result = checkin_f().criar_checkin(request.get_json())

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS, MSG_SUCESSO, result)
        )

    @api.expect(put_checkin_model, validate=True)
    def put(self):

        checkin_f().alterar_checkin(request.get_json())

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS,  MSG_SUCESSO, None)
        )

    @api.expect(model_delete_checkin, validate=True)
    def delete(self):
        id_param = request.args.get('id')
        checkin_f().apagar_checkin(id=id_param)

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS,  MSG_SUCESSO, None)
        )
