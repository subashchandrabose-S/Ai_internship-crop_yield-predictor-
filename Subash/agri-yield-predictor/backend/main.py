from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import numpy as np
import joblib
import os

# Initialize FastAPI app
app = FastAPI(
    title="Agri Yield Predictor API",
    description="API for agricultural yield prediction",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request body
class PredictionInput(BaseModel):
    temperature: float
    humidity: float
    rainfall: float
    soil_type: str
    crop_type: str
    weather_condition: str

# Pydantic model for response
class PredictionOutput(BaseModel):
    predicted_yield: float
    confidence: float
    status: str

# Mock model function (replace with your actual model)
def predict_yield(input_data: PredictionInput) -> dict:
    """
    Mock prediction function.
    Replace this with your actual model prediction logic.
    """
    # This is a placeholder - in a real app, you would load a trained model
    # model = joblib.load('model.pkl')
    # prediction = model.predict([[input_data.temperature, input_data.humidity, ...]])
    
    # For now, return mock data
    base_yield = 1000  # Base yield value
    temp_factor = input_data.temperature * 10
    rain_factor = input_data.rainfall * 2
    humidity_factor = input_data.humidity * 5
    
    predicted = base_yield + temp_factor + rain_factor + humidity_factor
    confidence = 0.85  # Mock confidence score
    
    return {
        "predicted_yield": round(predicted, 2),
        "confidence": round(confidence, 2),
        "status": "success"
    }

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Agri Yield Predictor API is running"}

# Prediction endpoint
@app.post("/api/predict", response_model=PredictionOutput)
async def predict_yield_endpoint(input_data: PredictionInput):
    try:
        result = predict_yield(input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Agri Yield Predictor API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
