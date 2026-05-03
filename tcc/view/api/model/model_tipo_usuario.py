from flask_restx import Model, fields, Namespace


def generate_tipo_usuario_model(api: Namespace, type: str) -> Model:
    model = {
        "codigo": fields.String(
            required=True, description="Código único do tipo de usuário",
            min_length=1
        ),
        "descricao": fields.String(
            required=True, description="Descrição do tipo de usuário",
            min_length=1
        ),

    }

    if type == 'post':
        model.update({"ch_usuario_inclusao": fields.String(
            required=False, description="Usuário que fez a inclusão"
        ), })
        return api.model(name='post_tipo_usuario_model', model=model)

    model.update({
        "id": fields.Integer(
            required=False, description="ID do tipo de usuário"
        ),
        "ch_usuario_alteracao": fields.String(
            required=False, description="Usuário que fez a alteração"
        )


    })
    return api.model(name='put_tipo_usuario_model', model=model)
