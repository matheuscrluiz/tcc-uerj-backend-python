from flask_restx import Model, fields, Namespace


def generate_andar_model(api: Namespace, type: str) -> Model:
    model = {
        "biblioteca_id": fields.Integer(
            required=True, description="ID da biblioteca"
        ),
        "numero": fields.Integer(
            required=True, description="Número do andar"
        ),
        "descricao": fields.String(
            required=False, description="Descrição do andar"
        ),

    }

    if type == 'post':
        model.update({"ch_usuario_inclusao": fields.String(
            required=False, description="Usuário que fez a inclusão"
        ), })
        return api.model(name='post_andar_model', model=model)

    model.update({
        "id": fields.Integer(
            required=False, description="ID do andar"
        ),
        "ch_usuario_alteracao": fields.String(
            required=False, description="Usuário que fez a alteração"
        )


    })
    return api.model(name='put_andar_model', model=model)
