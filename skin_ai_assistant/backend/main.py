from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
import logging
import sys
from datetime import datetime

from .inference import MODEL
from .db import Base, engine, get_db
from .models import InferenceRecord
from .config import BASE_DIR

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(BASE_DIR / "skin_ai.log")
    ]
)
logger = logging.getLogger(__name__)

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Failed to create database tables: {e}")

app = FastAPI(
    title="Skin AI Assistant API",
    version="1.0",
    description="AI-powered skin condition analysis API",
    contact={"name": "Skin AI Team"}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("=" * 70)
    logger.info("Skin AI Assistant API Starting")
    logger.info(f"Time: {datetime.now().isoformat()}")
    logger.info(f"Base Directory: {BASE_DIR}")
    logger.info(f"Model Loaded: {MODEL.session is not None}")
    logger.info("=" * 70)

IMAGES = BASE_DIR / "uploaded_images"
IMAGES.mkdir(exist_ok=True)

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    skin_type: str = Form("any"),
    fitzpatrick: str = Form("unspecified"),
    ethnicity: str = Form("unspecified"),
    db: Session = Depends(get_db),
):
    """Analyze uploaded image and return skin condition prediction."""
    try:
        logger.info(f"Analyzing image: {file.filename}, skin_type: {skin_type}")

        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Read and validate image
        img_bytes = await file.read()
        if len(img_bytes) == 0:
            raise HTTPException(status_code=400, detail="Empty file")
        if len(img_bytes) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")

        # Run prediction
        try:
            label, conf = MODEL.predict(img_bytes)
            logger.info(f"Prediction: {label} (confidence: {conf:.3f})")
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

        # Save for retraining
        rec = InferenceRecord(
            image_path=str(IMAGES / file.filename),
            predicted_condition=label,
            predicted_confidence=conf,
            user_skin_type=skin_type,
            user_fitzpatrick=fitzpatrick,
            user_ethnicity=ethnicity,
            predictions_json={"condition": label, "confidence": conf}
        )
        db.add(rec)
        db.commit()
        db.refresh(rec)

        # Save image file
        save_path = IMAGES / file.filename
        with open(save_path, "wb") as f:
            f.write(img_bytes)
        logger.info(f"Saved image: {save_path}")

        return {
            "inference_id": rec.id,
            "condition": label,
            "confidence": conf,
            "skin_type": skin_type,
            "fitzpatrick": fitzpatrick,
            "ethnicity": ethnicity
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
async def feedback(
    inference_id: str = Form(...),
    is_correct: bool = Form(...),
    corrected_condition: str = Form(None),
    db: Session = Depends(get_db),
):
    """Submit feedback on a prediction."""
    try:
        logger.info(f"Feedback for {inference_id}: correct={is_correct}, correction={corrected_condition}")

        r = db.query(InferenceRecord).filter_by(id=inference_id).first()
        if not r:
            logger.warning(f"Inference ID not found: {inference_id}")
            raise HTTPException(status_code=404, detail="Inference record not found")

        r.is_correct = is_correct
        if not is_correct:
            r.corrected_condition = corrected_condition
            r.needs_review = True

        db.commit()
        logger.info(f"Feedback saved for {inference_id}")
        return {"ok": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error saving feedback: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check endpoint for monitoring service status."""
    return {
        "status": "ok",
        "service": "Skin AI Assistant API",
        "version": "1.0",
        "model_loaded": MODEL.session is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/admin/inferences")
async def get_inferences(
    limit: int = 100,
    needs_review: str = None,
    db: Session = Depends(get_db),
):
    """Admin endpoint to retrieve inference records with optional filtering."""
    try:
        logger.info(f"Admin query: limit={limit}, needs_review={needs_review}")

        # Validate limit
        if limit < 1 or limit > 1000:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 1000")

        query = db.query(InferenceRecord)

        if needs_review == "true":
            query = query.filter(InferenceRecord.needs_review == True)
        elif needs_review == "false":
            query = query.filter(InferenceRecord.needs_review == False)

        records = query.order_by(InferenceRecord.created_at.desc()).limit(limit).all()
        logger.info(f"Returning {len(records)} inference records")

        return [
            {
                "id": r.id,
                "image_path": r.image_path,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "predicted_condition": r.predicted_condition,
                "predicted_confidence": r.predicted_confidence,
                "user_skin_type": r.user_skin_type,
                "user_fitzpatrick": r.user_fitzpatrick,
                "user_ethnicity": r.user_ethnicity,
                "is_correct": r.is_correct,
                "corrected_condition": r.corrected_condition,
                "needs_review": r.needs_review,
            }
            for r in records
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching inferences: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))