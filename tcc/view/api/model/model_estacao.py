from flask_restx import Model, fields, Namespace


def generate_estacao_model(api: Namespace, type: str) -> Model:
    model = {
        "andar_id": fields.Integer(
            required=True, description="ID do andar"
        ),
        "tipo_estacao_id": fields.Integer(
            required=True, description="ID do tipo de estação"
        ),
        "codigo": fields.String(
            required=True, description="Código da estação",
            min_length=1
        ),
        "capacidade": fields.Integer(
            required=False, description="Capacidade da estação"
        ),
        "status": fields.String(
            required=True, description="Status da estação (ATIVA/MANUTENCAO)",
            min_length=1
        ),

    }

    if type == 'post':
        model.update({"ch_usuario_inclusao": fields.String(
            required=False, description="Usuário que fez a inclusão"
        ), })
        return api.model(name='post_estacao_model', model=model)

    model.update({
        "id": fields.Integer(
            required=False, description="ID da estação"
        ),
        "ch_usuario_alteracao": fields.String(
            required=False, description="Usuário que fez a alteração"
        )


    })
    return api.model(name='put_estacao_model', model=model)
