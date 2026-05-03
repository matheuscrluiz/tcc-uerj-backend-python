from flask_restx import Model, fields, Namespace


def generate_usuario_model(api: Namespace, type: str) -> Model:
    model = {
        "nome": fields.String(
            required=True, description="Nome completo do usuário",
            min_length=1
        ),
        "email": fields.String(
            required=True, description="Email único do usuário",
            min_length=1
        ),
        "senha_hash": fields.String(
            required=True, description="Hash da senha do usuário",
            min_length=1
        ),
        "tipo_usuario_id": fields.Integer(
            required=True, description="ID do tipo de usuário"
        ),
        "ativo": fields.String(
            required=True, description="Status ativo do usuário",
            max_length=1

        ),

    }

    if type == 'post':
        model.update({
            "ch_usuario_inclusao": fields.String(
                required=False, description="Usuário que fez a inclusão"
            ),
            "ch_rede": fields.String(
                required=True, description="Chave da rede do usuário",
                min_length=1
            ),
            "matricula": fields.String(
                required=True, description="Matrícula única do usuário",
                min_length=1
            ),
        }),
        return api.model(name='post_usuario_model', model=model)

    model.update({
        "id": fields.Integer(
            required=False, description="ID do usuário"
        ),
        "ch_usuario_alteracao": fields.String(
            required=False, description="Usuário que fez a alteração"
        )


    })
    return api.model(name='put_usuario_model', model=model)
