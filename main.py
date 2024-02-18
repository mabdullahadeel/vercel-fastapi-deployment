from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

# Definir el modelo de datos utilizando Pydantic
class Position(BaseModel):
    description: str
    position: float
    avgCost: float
    marketPrice: float
    marketValue: float
    realizedPnl: float
    unrealizedPnl: float
    sector: str = None
    group: str = None

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Datos de ejemplo
positions_data = [
    {
        "description": "AMZN",
        "position": 0.5946,
        "avgCost": 160.54,
        "marketPrice": 168.77,
        "marketValue": 100.35,
        "realizedPnl": 0.0,
        "unrealizedPnl": 4.89,
        "sector": "Communications",
        "group": "Internet"
    },
    {
        "description": "BABA",
        "position": 3.0708,
        "avgCost": 121.98,
        "marketPrice": 73.82,
        "marketValue": 226.69,
        "realizedPnl": 0.0,
        "unrealizedPnl": -147.90,
        "sector": "Communications",
        "group": "Internet"
    },
    # Agrega más datos de ejemplo aquí si es necesario
]




# Definir una ruta para procesar los datos JSON



@app.post("/process_positions/")
async def process_positions(positions: List[Position]):
    processed_data = []
    for pos in positions:
        # Aquí puedes realizar cualquier procesamiento adicional necesario
        processed_data.append({
            "Description": pos.description,
            "Position": pos.position,
            "Average Cost": pos.avgCost,
            "Market Price": pos.marketPrice,
            "Market Value": pos.marketValue,
            "Realized PnL": pos.realizedPnl,
            "Unrealized PnL": pos.unrealizedPnl,
            "Sector": pos.sector,
            "Group": pos.group
        })
    return {"processed_data": processed_data, "original_data": positions}

@app.get("/positions/", response_model=List[Position])
async def get_positions():
    return positions_data