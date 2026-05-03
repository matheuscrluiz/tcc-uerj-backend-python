from flask_restx import Model, fields, Namespace


def generate_biblioteca_model(api: Namespace, type: str) -> Model:
    model = {
        "nome": fields.String(
            required=True, description="Nome da biblioteca",
            min_length=1
        ),
        "descricao": fields.String(
            required=False, description="Descrição da biblioteca"
        ),

    }

    if type == 'post':
        model.update({"ch_usuario_inclusao": fields.String(
            required=False, description="Usuário que fez a inclusão"
        ), })
        return api.model(name='post_biblioteca_model', model=model)

    model.update({
        "id": fields.Integer(
            required=False, description="ID da biblioteca"
        ),
        "ch_usuario_alteracao": fields.String(
            required=False, description="Usuário que fez a alteração"
        )


    })
    return api.model(name='put_biblioteca_model', model=model)
