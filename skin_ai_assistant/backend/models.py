import uuid
from sqlalchemy import Column, String, DateTime, Boolean, JSON, Float
from datetime import datetime
from .db import Base

class InferenceRecord(Base):
    __tablename__ = "inferences"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    image_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    predicted_condition = Column(String, nullable=False)
    predicted_confidence = Column(Float, nullable=True)

    # Extra fields for multitask upgrades
    predicted_skin_type = Column(String)
    predicted_fitzpatrick = Column(String)
    predicted_acne_grade = Column(Float)
    predicted_pih_level = Column(Float)

    user_skin_type = Column(String)
    user_fitzpatrick = Column(String)
    user_ethnicity = Column(String)

    predictions_json = Column(JSON)

    # Feedback
    is_correct = Column(Boolean, default=None)
    corrected_condition = Column(String)
    corrected_acne_grade = Column(Float)
    corrected_pih_level = Column(Float)
    notes = Column(String)
    needs_review = Column(Boolean, default=False)