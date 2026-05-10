from flask_restx import Model, fields, Namespace


def generate_log_ocupacao_model(api: Namespace, type: str) -> Model:
    model = {
        "estacao_id": fields.Integer(
            required=True, description="ID da estação"
        ),
        "usuario_id": fields.Integer(
            required=False, description="ID do usuário"
        ),
        "data": fields.Date(
            required=True, description="Data da ocupação"
        ),
        "hora_inicio": fields.String(
            required=True, description="Hora de início (HH:MM:SS)",
            min_length=1
        ),
        "hora_fim": fields.String(
            required=True, description="Hora de fim (HH:MM:SS)",
            min_length=1
        ),
        "foi_reserva": fields.String(
            required=True, description="Foi reserva (S/N)",
            min_length=1,
            max_length=1
        ),

    }

    if type == 'post':
        model.update({"ch_usuario_inclusao": fields.String(
            required=False, description="Usuário que fez a inclusão"
        ), })
        return api.model(name='post_log_ocupacao_model', model=model)

    model.update({
        "id": fields.Integer(
            required=False, description="ID do log"
        ),
        "ch_usuario_alteracao": fields.String(
            required=False, description="Usuário que fez a alteração"
        )


    })
    return api.model(name='put_log_ocupacao_model', model=model)
