from flask_restx import Model, fields, Namespace


def generate_reserva_model(api: Namespace, type: str) -> Model:
    model = {
        "usuario_id": fields.Integer(
            required=True, description="ID do usuário"
        ),
        "estacao_id": fields.Integer(
            required=True, description="ID da estação"
        ),
        "data": fields.Date(
            required=True, description="Data da reserva"
        ),
        "hora_inicio": fields.String(
            required=True, description="Hora de início (HH:MM:SS)",
            min_length=1
        ),
        "hora_fim": fields.String(
            required=True, description="Hora de fim (HH:MM:SS)",
            min_length=1
        ),
        "status": fields.String(
            required=True, description="Status da reserva ",
            min_length=1
        ),

    }

    if type == 'post':
        model.update({"ch_usuario_inclusao": fields.String(
            required=False, description="Usuário que fez a inclusão"
        ), })
        return api.model(name='post_reserva_model', model=model)

    model.update({
        "id": fields.Integer(
            required=False, description="ID da reserva"
        ),
        "ch_usuario_alteracao": fields.String(
            required=False, description="Usuário que fez a alteração"
        )


    })
    return api.model(name='put_reserva_model', model=model)
