# coding: utf-8
from flask import jsonify, request
from flask_restx import Resource
from flask_restx.namespace import Namespace

from tcc.util.util import get_dict_retorno_endpoint
from tcc.view.api.model.model_biblioteca import generate_biblioteca_model
from ...util.constants import MSG_SUCESSO, TIP_RETORNO_SUCESS
from ...model.facade.biblioteca_facade import (
    BibliotecaFacade as biblioteca_f)
# ---------------------------->>
# NameSpace
# ---------------------------->>

api = Namespace('biblioteca', description='biblioteca')

# ---------------------------->>
# Model
# ---------------------------->>


post_biblioteca_model = generate_biblioteca_model(api, "post")
put_biblioteca_model = generate_biblioteca_model(api, "put")

model_get_biblioteca = api.parser().add_argument(
    name='id',
    type=int,
    required=False
)
model_delete_biblioteca = api.parser().add_argument(
    name='id',
    type=int,
    required=True
)

# ---------------------------->>
# Rotas
# ---------------------------->>


@api.route('')
class ResourceBiblioteca(Resource):

    @api.expect(model_get_biblioteca, validate=True)
    def get(self):
        id_param = request.args.get('id')
        result = biblioteca_f().obter_biblioteca(id=id_param)

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS, MSG_SUCESSO, result)
        )

    @api.expect(post_biblioteca_model, validate=True)
    def post(self):

        result = biblioteca_f().criar_biblioteca(request.get_json())

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS, MSG_SUCESSO, result)
        )

    @api.expect(put_biblioteca_model, validate=True)
    def put(self):

        biblioteca_f().alterar_biblioteca(request.get_json())

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS,  MSG_SUCESSO, None)
        )

    @api.expect(model_delete_biblioteca, validate=True)
    def delete(self):
        id_param = request.args.get('id')
        biblioteca_f().apagar_biblioteca(id=id_param)

        return jsonify(
            get_dict_retorno_endpoint(TIP_RETORNO_SUCESS,  MSG_SUCESSO, None)
        )
