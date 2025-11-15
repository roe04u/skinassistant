from sqlalchemy.orm import Session
from backend.db import SessionLocal
from backend.models import InferenceRecord
from backend.config import BASE_DIR
from pathlib import Path
import shutil

DATA = BASE_DIR / "dataset"

def build():
    if DATA.exists(): shutil.rmtree(DATA)
    (DATA/'train').mkdir(parents=True)
    (DATA/'val').mkdir(parents=True)

    db: Session = SessionLocal()
    recs = db.query(InferenceRecord).filter_by(is_correct=True).all()

    train_split = int(len(recs)*0.8)
    train, val = recs[:train_split], recs[train_split:]

    def copy(records, root):
        for r in records:
            label = r.corrected_condition or r.predicted_condition
            src = BASE_DIR / r.image_path
            dst = root/label
            dst.mkdir(exist_ok=True)
            shutil.copy2(src, dst/src.name)

    copy(train, DATA/'train')
    copy(val, DATA/'val')

if __name__ == "__main__":
    build()