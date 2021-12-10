""" Módulo principal da API de predição
"""
import joblib
from fastapi import FastAPI
from pydantic import BaseModel, validator

description = """
# Desafio Machine Learning Engineer. 🚀

API para predição do motivo de alta de pacientes, com base em:

- idade
- setor
- temperatura
- frequência respiratória
- pressão arterial sistólica
- pressão arterial diastólica
- pressão arterial média
- saturação da oxigenação

O motivo de alta assumido é:
- Óbito
- Melhorado

"""

app = FastAPI(
    title="PredictAPI",
    description=description,
    version="0.0.1",
    contact={
        "name": "Ivan Pereira",
        "email": "navi1921@gmail.com",
    },
)

model = joblib.load("sepse_model.joblib")
label_encoder = joblib.load("le.joblib")


class PatientData(BaseModel):
    """Model dos dados utilizados pelo endpoint /predict"""

    age: int
    sector: str
    temperature: float
    respiratory_frequency: float
    systolic_blood_pressure: float
    diastolic_blood_pressure: float
    mean_arterial_pressure: float
    oxygen_saturation: float

    @validator("sector")
    def invalid_sector(cls, value):
        value = value.upper().strip()
        if value not in [
            "UTIG",
            "1AP2",
            "4AP2",
            "UTIC",
            "UTIP",
            "3AP1",
            "3AP2",
            "4AP1",
            "1AP1",
            "2AP2",
            "UIP",
            "3AP3",
            "1AP2 - 126",
            "2AP1",
            "3AP3 - EPI",
            "SEMI-CO",
        ]:
            raise ValueError("the sector does not exist in the database")
        return value


@app.post("/predict")
def predict_data(data: PatientData):
    """Informe os dados do paciente que deseja obter uma predição."""
    sector_encoded = label_encoder.transform([data.sector])
    features = [
        data.age,
        sector_encoded,
        data.temperature,
        data.respiratory_frequency,
        data.systolic_blood_pressure,
        data.diastolic_blood_pressure,
        data.mean_arterial_pressure,
        data.oxygen_saturation,
    ]

    y_pred = model.predict([features])
    return {"predição": y_pred[0]}
