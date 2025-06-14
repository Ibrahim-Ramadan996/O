from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import joblib
import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NurseResponse(BaseModel):
    NurseID: int
    FName: str
    LName: str
    PhoneNumber: int
    Email: str
    Experience: int
    Specialty: str
    City: str
    Street: str
    AverageRating: float
    ReviewCount: float
    Comment: str
    Score: float

app = FastAPI(
    title="نظام ترشيح الممرضين",
    description="API لتوصية الممرضين حسب المدينة",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable for DataFrame
df = None

def load_data():
    """Load and prepare the data"""
    global df
    try:
        # Check if file exists
        if not os.path.exists("nurse_data_frame.joblib"):
            raise FileNotFoundError("Data file not found")
            
        # Load data
        df = joblib.load("nurse_data_frame.joblib")
        
        # Verify required columns
        required_columns = {
            "NurseID", "FName", "LName", "PhoneNumber", "Email",
            "Experience", "Specialty", "City", "Street",
            "AverageRating", "ReviewCount", "Comment", "Score"
        }
        
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
            
        # Clean and prepare data
        df = df[df['City'].notna()].copy()
        df["City_clean"] = df["City"].astype(str).str.strip().str.lower()
        
        logger.info("Data loaded successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        return False

@app.on_event("startup")
async def startup_event():
    """Load data when the application starts"""
    if not load_data():
        logger.error("Failed to load data during startup")

@app.get("/")
async def root():
    """Root endpoint to check if the API is running"""
    return {
        "status": "running",
        "message": "مرحباً بك في نظام ترشيح الممرضين",
        "data_loaded": df is not None
    }

@app.get("/nurses/{city}", response_model=List[NurseResponse])
async def get_nurses_by_city(city: str):
    """Get nurses by city"""
    try:
        if df is None:
            if not load_data():
                raise HTTPException(
                    status_code=500,
                    detail="فشل تحميل البيانات. يرجى المحاولة مرة أخرى لاحقاً"
                )

        # Clean and normalize city name
        city_normalized = city.strip().lower()
        
        # Filter nurses
        filtered = df[df["City_clean"] == city_normalized].sort_values("Score", ascending=False)

        if filtered.empty:
            raise HTTPException(
                status_code=404,
                detail=f"❌ لا يوجد ممرضين في المدينة: {city}"
            )

        # Convert to response format
        result = filtered.drop(columns=["City_clean"]).to_dict("records")
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="⚠️ حدث خطأ أثناء معالجة الطلب"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 