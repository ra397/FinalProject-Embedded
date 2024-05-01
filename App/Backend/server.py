from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()

class TemperatureData(BaseModel):
    c_temperature: float
    f_temperature: float

temp_data = []

@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse('App/Frontend/index.html')

@app.get("/temperature")
async def transmit_temperature() -> dict:
    if temp_data:
        # Return the last temperature reading
        return temp_data[-1].dict()
    return {"message": "No temperature data available"}

@app.post("/temperature")
async def receive_temperature(data: TemperatureData):
    temp = TemperatureData(c_temperature=data.c_temperature, f_temperature=data.f_temperature)
    temp_data.append(temp)
    return {"message": "Data received successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.0.103", port=8000)