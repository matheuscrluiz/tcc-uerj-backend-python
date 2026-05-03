# coding: utf-8
from flask import jsonify, request
from flask_restx import Resource
from flask_restx.namespace import Namespace

from tcc.util.util import get_dict_retorno_endpoint
from tcc.view.api.model.model_andar import generate_andar_model
from ...util.constants import MSG_SUCESSO, TIP_RETORNO_SUCESS
from ...model.facade.andar_facade import (
    AndarFacade as andar_f)
# ---------------------------->>
# NameSpace
# ---------------------------->>

api = Namespace('andar', description='andar')

# ---------------------------->>
# Model
# ---------------------------->>


post_andar_model = generate_andar_model(api, "post")
put_andar_model = generate_andar_model(api, "put")

model_get_andar = api.parser().add_argument(
    name='id',
    type=int,
    required=False
)
model_delete_andar = api.parser().add_argument(
    name='id',
    type=int,
    required=True
)

# ---------------------------->>
# Rotas
# ---------------------------->>


@api.route('')
class ResourceAndar(Resource):

    @api.expect(model_get_andar, validate=True)
    def get(self):
        id_param = request.args.get('id')
        result = andar_f().obter_andar(id=id_param)

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS, MSG_SUCESSO, result)
        )

    @api.expect(post_andar_model, validate=True)
    def post(self):

        result = andar_f().criar_andar(request.get_json())

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS, MSG_SUCESSO, result)
        )

    @api.expect(put_andar_model, validate=True)
    def put(self):

        andar_f().alterar_andar(request.get_json())

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS,  MSG_SUCESSO, None)
        )

    @api.expect(model_delete_andar, validate=True)
    def delete(self):
        id_param = request.args.get('id')
        andar_f().apagar_andar(id=id_param)

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS,  MSG_SUCESSO, None)
        )
