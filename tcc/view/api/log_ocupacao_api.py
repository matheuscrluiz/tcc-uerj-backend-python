# coding: utf-8
from flask import jsonify, request
from flask_restx import Resource
from flask_restx.namespace import Namespace

from tcc.util.util import get_dict_retorno_endpoint
from tcc.view.api.model.model_log_ocupacao import generate_log_ocupacao_model
from ...util.constants import MSG_SUCESSO, TIP_RETORNO_SUCESS
from ...model.facade.log_ocupacao_facade import (
    LogOcupacaoFacade as log_ocupacao_f)
# ---------------------------->>
# NameSpace
# ---------------------------->>

api = Namespace('log_ocupacao', description='log_ocupacao')

# ---------------------------->>
# Model
# ---------------------------->>


post_log_ocupacao_model = generate_log_ocupacao_model(api, "post")
put_log_ocupacao_model = generate_log_ocupacao_model(api, "put")

model_get_log_ocupacao = api.parser().add_argument(
    name='id',
    type=int,
    required=False
)
model_delete_log_ocupacao = api.parser().add_argument(
    name='id',
    type=int,
    required=True
)

# ---------------------------->>
# Rotas
# ---------------------------->>


@api.route('')
class ResourceLogOcupacao(Resource):

    @api.expect(model_get_log_ocupacao, validate=True)
    def get(self):
        id_param = request.args.get('id')
        result = log_ocupacao_f().obter_log_ocupacao(id=id_param)

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS, MSG_SUCESSO, result)
        )

    @api.expect(post_log_ocupacao_model, validate=True)
    def post(self):

        result = log_ocupacao_f().criar_log_ocupacao(request.get_json())

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS, MSG_SUCESSO, result)
        )

    @api.expect(put_log_ocupacao_model, validate=True)
    def put(self):

        log_ocupacao_f().alterar_log_ocupacao(request.get_json())

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS,  MSG_SUCESSO, None)
        )

    @api.expect(model_delete_log_ocupacao, validate=True)
    def delete(self):
        id_param = request.args.get('id')
        log_ocupacao_f().apagar_log_ocupacao(id=id_param)

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS,  MSG_SUCESSO, None)
        )
