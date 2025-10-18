from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Response
import base64
from infer import run_inference_and_annotate
from PIL import Image
import io
from typing import Optional
import logging 
logging.basicConfig(level=logging.INFO)

import requests
from clinics import (
    find_nearest_clinics,
    validate_coordinates
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/infer")
async def infer_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        img_bytes, detections = run_inference_and_annotate(image)

        # Encode image as base64
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        # Return multipart JSON
        return {
            "image": img_base64,
            "detections": detections
        }
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    
CONDITION_DATABASE = {
    "Actinic keratoses and intraepithelial carcinoma / Bowen's disease (akiec)": {
        "fullname": "Actinic keratoses and intraepithelial carcinoma / Bowen's disease",
        "description": "Precancerous skin lesions that may progress to squamous cell carcinoma. Often appear as rough, scaly patches.",
        "symptoms": [
            "Scaly or crusty growths",
            "Red or pink patches",
            "Itching or burning",
            "Bleeding or ulceration"
        ]
    },
    "Basal cell carcinoma (bcc)": {
        "fullname": "Basal cell carcinoma",
        "description": "A common type of skin cancer that arises from basal cells. Usually appears as a pearly bump.",
        "symptoms": [
            "Pearly or waxy bump",
            "Flat, flesh-colored lesion",
            "Bleeding or scabbing sore"
        ]
    },
    "Melanocytic nevi (NV)": {
        "fullname": "Melanocytic nevi",
        "description": "TEST",
        "symptoms": [
            "S1",
            "S2"
        ]
    },
    # Add more conditions as needed...
}

@app.get("/condition-info")
def get_condition_info(name: str = Query(..., description="Full name and abbreviation")):
    response = requests.post("http://ollama:11434/api/chat", json={
        "model": "qwen3:0.6b", 
        "messages": [
            {"role": "user", "content": f"Explain the condition {name} simply and under 50 words."}
        ],
        "stream": False
    })
    return JSONResponse(
        status_code=200,
        content={"message": response.json()['message']['content']}
    )

@app.get("/clinics")
def get_clinics(
    lat: Optional[float] = Query(None, description="User's latitude"),
    lng: Optional[float] = Query(None, description="User's longitude"),
):
    try:
        if lat is not None and lng is not None:
            # Validate coordinates
            is_valid, error_msg = validate_coordinates(lat, lng)

            if not is_valid:
                return JSONResponse(
                    status_code=400,
                    content={"error": error_msg}
                )
            
            nearest_clinics = find_nearest_clinics(
                lat, lng
            )
            
            return nearest_clinics

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Server error: {str(e)}"}
        )