# coding: utf-8
from flask import jsonify, request
from flask_restx import Resource
from flask_restx.namespace import Namespace

from tcc.util.util import get_dict_retorno_endpoint
from tcc.view.api.model.model_tipo_estacao import generate_tipo_estacao_model
from ...util.constants import MSG_SUCESSO, TIP_RETORNO_SUCESS
from ...model.facade.tipo_estacao_facade import (
    TipoEstacaoFacade as tipo_estacao_f)
# ---------------------------->>
# NameSpace
# ---------------------------->>

api = Namespace('tipo_estacao', description='tipo_estacao')

# ---------------------------->>
# Model
# ---------------------------->>


post_tipo_estacao_model = generate_tipo_estacao_model(api, "post")
put_tipo_estacao_model = generate_tipo_estacao_model(api, "put")

model_get_tipo_estacao = api.parser().add_argument(
    name='id',
    type=int,
    required=False
)
model_delete_tipo_estacao = api.parser().add_argument(
    name='id',
    type=int,
    required=True
)

# ---------------------------->>
# Rotas
# ---------------------------->>


@api.route('')
class ResourceTipoEstacao(Resource):

    @api.expect(model_get_tipo_estacao, validate=True)
    def get(self):
        id_param = request.args.get('id')
        result = tipo_estacao_f().obter_tipo_estacao(id=id_param)

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS, MSG_SUCESSO, result)
        )

    @api.expect(post_tipo_estacao_model, validate=True)
    def post(self):

        result = tipo_estacao_f().criar_tipo_estacao(request.get_json())

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS, MSG_SUCESSO, result)
        )

    @api.expect(put_tipo_estacao_model, validate=True)
    def put(self):

        tipo_estacao_f().alterar_tipo_estacao(request.get_json())

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS,  MSG_SUCESSO, None)
        )

    @api.expect(model_delete_tipo_estacao, validate=True)
    def delete(self):
        id_param = request.args.get('id')
        tipo_estacao_f().apagar_tipo_estacao(id=id_param)

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS,  MSG_SUCESSO, None)
        )
