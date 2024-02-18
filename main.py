from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
import sqlite3

# Modelo de datos con Pydantic
class Position(BaseModel):
    description: str
    position: float
    avgCost: float
    marketPrice: float
    marketValue: float
    realizedPnl: float
    unrealizedPnl: float
    sector: str = None
    group_name: str = None

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Conexión a la base de datos SQLite
conn = sqlite3.connect('positions.db')
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS positions
                  (description TEXT PRIMARY KEY,
                  position REAL,
                  avgCost REAL,
                  marketPrice REAL,
                  marketValue REAL,
                  realizedPnl REAL,
                  unrealizedPnl REAL,
                  sector TEXT,
                  group_name TEXT)''')  # Corregido el nombre de la columna de "group_name" a "group_name"
conn.commit()


# Operaciones CRUD

# Create
@app.post("/positions/", response_model=Position)
async def create_position(position: Position):
    try:
        cursor.execute("INSERT INTO positions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                       (position.description, position.position, position.avgCost, 
                        position.marketPrice, position.marketValue, position.realizedPnl, 
                        position.unrealizedPnl, position.sector, position.group_name))
        conn.commit()
        return position
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Position already exists")

# Read All
@app.get("/positions/", response_model=List[Position])
async def get_positions():
    cursor.execute("SELECT * FROM positions")
    rows = cursor.fetchall()
    positions = []
    for row in rows:
        positions.append(Position(description=row[0], position=row[1], avgCost=row[2], 
                                  marketPrice=row[3], marketValue=row[4], realizedPnl=row[5], 
                                  unrealizedPnl=row[6], sector=row[7], group_name=row[8]))
    return positions

# Read One
@app.get("/positions/{description}", response_model=Position)
async def get_position(description: str):
    cursor.execute("SELECT * FROM positions WHERE description=?", (description,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return Position(description=row[0], position=row[1], avgCost=row[2], 
                    marketPrice=row[3], marketValue=row[4], realizedPnl=row[5], 
                    unrealizedPnl=row[6], sector=row[7], group_name=row[8])

# Update
@app.put("/positions/{description}", response_model=Position)
async def update_position(description: str, position: Position):
    cursor.execute("UPDATE positions SET position=?, avgCost=?, marketPrice=?, marketValue=?, "
                   "realizedPnl=?, unrealizedPnl=?, sector=?, group_name=? WHERE description=?", 
                   (position.position, position.avgCost, position.marketPrice, 
                    position.marketValue, position.realizedPnl, position.unrealizedPnl, 
                    position.sector, position.group_name, description))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Position not found")
    return position

# Delete
@app.delete("/positions/{description}")
async def delete_position(description: str):
    cursor.execute("DELETE FROM positions WHERE description=?", (description,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Position not found")
    return {"message": "Position deleted successfully"}

# Cerrar la conexión a la base de datos al finalizar la aplicación
@app.on_event("shutdown")
def close_connection():
    conn.close()


# Iniciar el servidor FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
