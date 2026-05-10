from flask_restx import Model, fields, Namespace


def generate_checkin_model(api: Namespace, type: str) -> Model:
    model = {
        "reserva_id": fields.Integer(
            required=True, description="ID da reserva"
        ),
        "hora_checkin": fields.DateTime(
            required=False, description="Data e hora do check-in"
        ),
        "hora_checkout": fields.DateTime(
            required=False, description="Data e hora do check-out"
        ),
        "status": fields.String(
            required=True, description="Status do check-in (PRESENTE/NO_SHOW)",
            min_length=1
        ),

    }

    if type == 'post':
        model.update({"ch_usuario_inclusao": fields.String(
            required=False, description="Usuário que fez a inclusão"
        ), })
        return api.model(name='post_checkin_model', model=model)

    model.update({
        "id": fields.Integer(
            required=False, description="ID do check-in"
        ),
        "ch_usuario_alteracao": fields.String(
            required=False, description="Usuário que fez a alteração"
        )


    })
    return api.model(name='put_checkin_model', model=model)
