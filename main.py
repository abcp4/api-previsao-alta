""" Módulo principal da API de predição
"""
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
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


@app.post("/predict")
def predict_data(data: PatientData):
    """Informe os dados do paciente que deseja obter uma predição."""
    try:
        sector_encoded = label_encoder.transform([data.sector])
    except ValueError:
        raise HTTPException(status_code=404, detail="Setor não encontrado")

    y_pred = model.predict(
        [
            [
                data.age,
                sector_encoded,
                data.temperature,
                data.respiratory_frequency,
                data.systolic_blood_pressure,
                data.diastolic_blood_pressure,
                data.mean_arterial_pressure,
                data.oxygen_saturation,
            ]
        ]
    )
    return {"predição": y_pred[0]}
