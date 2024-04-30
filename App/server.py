from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TemperatureData(BaseModel):
    c_temperature: float
    f_temperature: float

@app.get("/")
async def root():
    return {'message': 'Temperature sensor app'}

@app.post("/temperature")
async def receive_temperature(data: TemperatureData):
    print(f"Received temperature: {data.c_temperature}°C {data.f_temperature}")
    return {"message": "Data received successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.0.105", port=8000)