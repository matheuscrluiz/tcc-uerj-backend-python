from flask_restx import fields


MODEL_AREA = {

    "nome": fields.String(
        required=True, description="NOM_AREA", min_length=1
    )
}
