# coding: utf-8
from flask import jsonify, request
from flask_restx import Resource
from flask_restx.namespace import Namespace

from tcc.util.util import get_dict_retorno_endpoint
from tcc.view.api.model.model_usuario import generate_usuario_model
from ...util.constants import MSG_SUCESSO, TIP_RETORNO_SUCESS
from ...model.facade.usuario_facade import (
    UsuarioFacade as usuario_f)
# ---------------------------->>
# NameSpace
# ---------------------------->>

api = Namespace('usuario', description='usuario')

# ---------------------------->>
# Model
# ---------------------------->>


post_usuario_model = generate_usuario_model(api, "post")
put_usuario_model = generate_usuario_model(api, "put")

model_get_usuario = api.parser().add_argument(
    name='id',
    type=int,
    required=False
)
model_delete_usuario = api.parser().add_argument(
    name='id',
    type=int,
    required=True
)

# ---------------------------->>
# Rotas
# ---------------------------->>


@api.route('')
class ResourceUsuario(Resource):

    @api.expect(model_get_usuario, validate=True)
    def get(self):
        id_param = request.args.get('id')
        result = usuario_f().obter_usuario(id=id_param)

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS, MSG_SUCESSO, result)
        )

    @api.expect(post_usuario_model, validate=True)
    def post(self):

        result = usuario_f().criar_usuario(request.get_json())

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS, MSG_SUCESSO, result)
        )

    @api.expect(put_usuario_model, validate=True)
    def put(self):

        usuario_f().alterar_usuario(request.get_json())

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS,  MSG_SUCESSO, None)
        )

    @api.expect(model_delete_usuario, validate=True)
    def delete(self):
        id_param = request.args.get('id')
        usuario_f().apagar_usuario(id=id_param)

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS,  MSG_SUCESSO, None)
        )
