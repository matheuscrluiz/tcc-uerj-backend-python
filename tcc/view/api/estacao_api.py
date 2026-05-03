# coding: utf-8
from flask import jsonify, request
from flask_restx import Resource
from flask_restx.namespace import Namespace

from tcc.util.util import get_dict_retorno_endpoint
from tcc.view.api.model.model_estacao import generate_estacao_model
from ...util.constants import MSG_SUCESSO, TIP_RETORNO_SUCESS
from ...model.facade.estacao_facade import (
    EstacaoFacade as estacao_f)
# ---------------------------->>
# NameSpace
# ---------------------------->>

api = Namespace('estacao', description='estacao')

# ---------------------------->>
# Model
# ---------------------------->>


post_estacao_model = generate_estacao_model(api, "post")
put_estacao_model = generate_estacao_model(api, "put")

model_get_estacao = api.parser().add_argument(
    name='id',
    type=int,
    required=False
)
model_delete_estacao = api.parser().add_argument(
    name='id',
    type=int,
    required=True
)

# ---------------------------->>
# Rotas
# ---------------------------->>


@api.route('')
class ResourceEstacao(Resource):

    @api.expect(model_get_estacao, validate=True)
    def get(self):
        id_param = request.args.get('id')
        result = estacao_f().obter_estacao(id=id_param)

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS, MSG_SUCESSO, result)
        )

    @api.expect(post_estacao_model, validate=True)
    def post(self):

        result = estacao_f().criar_estacao(request.get_json())

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS, MSG_SUCESSO, result)
        )

    @api.expect(put_estacao_model, validate=True)
    def put(self):

        estacao_f().alterar_estacao(request.get_json())

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS,  MSG_SUCESSO, None)
        )

    @api.expect(model_delete_estacao, validate=True)
    def delete(self):
        id_param = request.args.get('id')
        estacao_f().apagar_estacao(id=id_param)

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS,  MSG_SUCESSO, None)
        )
