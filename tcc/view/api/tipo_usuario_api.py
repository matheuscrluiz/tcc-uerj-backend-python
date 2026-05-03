# coding: utf-8
from flask import jsonify, request
from flask_restx import Resource
from flask_restx.namespace import Namespace

from tcc.util.util import get_dict_retorno_endpoint
from tcc.view.api.model.model_tipo_usuario import generate_tipo_usuario_model
from ...util.constants import MSG_SUCESSO, TIP_RETORNO_SUCESS
from ...model.facade.tipo_usuario_facade import (
    TipoUsuarioFacade as tipo_usuario_f)
# ---------------------------->>
# NameSpace
# ---------------------------->>

api = Namespace('tipo_usuario', description='tipo_usuario')

# ---------------------------->>
# Model
# ---------------------------->>


post_tipo_usuario_model = generate_tipo_usuario_model(api, "post")
put_tipo_usuario_model = generate_tipo_usuario_model(api, "put")

model_get_tipo_usuario = api.parser().add_argument(
    name='id',
    type=int,
    required=False
)
model_delete_tipo_usuario = api.parser().add_argument(
    name='id',
    type=int,
    required=True
)

# ---------------------------->>
# Rotas
# ---------------------------->>


@api.route('')
class ResourceTipoUsuario(Resource):

    @api.expect(model_get_tipo_usuario, validate=True)
    def get(self):
        id_param = request.args.get('id')
        result = tipo_usuario_f().obter_tipo_usuario(id=id_param)

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS, MSG_SUCESSO, result)
        )

    @api.expect(post_tipo_usuario_model, validate=True)
    def post(self):

        result = tipo_usuario_f().criar_tipo_usuario(request.get_json())

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS, MSG_SUCESSO, result)
        )

    @api.expect(put_tipo_usuario_model, validate=True)
    def put(self):

        tipo_usuario_f().alterar_tipo_usuario(request.get_json())

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS,  MSG_SUCESSO, None)
        )

    @api.expect(model_delete_tipo_usuario, validate=True)
    def delete(self):
        id_param = request.args.get('id')
        tipo_usuario_f().apagar_tipo_usuario(id=id_param)

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS,  MSG_SUCESSO, None)
        )
