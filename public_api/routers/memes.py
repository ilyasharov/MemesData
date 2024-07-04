from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Query
from sqlalchemy.orm import Session

from public_api.database import SessionLocal, database
from public_api.schemas.meme import Meme, MemeCreate, MemeUpdate, MemeList
from public_api.models.meme import Meme as MemeModel
from public_api.services.s3_service import upload_image_to_s3

from typing import Optional, List

router = APIRouter()

memes_db = []

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=Meme)
async def create_meme(
    title: str,
    description: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    filename = f"{title}_{file.filename}"
    image_url = upload_image_to_s3(file, filename)

    db_meme = MemeModel(title=title, description=description, image_url=image_url)
    db.add(db_meme)
    db.commit()
    db.refresh(db_meme)
    return db_meme


@router.put("/{id}", response_model=Meme)
async def update_meme(
    id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    file: Optional[UploadFile] = None,
    db: Session = Depends(get_db)
):
    db_meme = db.query(MemeModel).filter(MemeModel.id == id).first()

    if db_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")

    if title:
        db_meme.title = title

    if description:
        db_meme.description = description

    if file:
        filename = f"{db_meme.title}_{file.filename}"
        image_url = upload_image_to_s3(file, filename)
        db_meme.image_url = image_url

    db.commit()
    db.refresh(db_meme)
    return db_meme


@router.get("/{id}", response_model=Meme)
async def get_meme(id: int, db: Session = Depends(get_db)):
    db_meme = db.query(MemeModel).filter(MemeModel.id == id).first()

    if db_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")

    return db_meme

@router.get("/", response_model=MemeList)
async def list_memes(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    total = db.query(MemeModel).count()
    memes = db.query(MemeModel).offset((page - 1) * size).limit(size).all()
    
    return MemeList(items=memes, total=total, page=page, size=size)

@router.delete("/{id}", response_model=Meme)
async def delete_meme(id: int, db: Session = Depends(get_db)):
    db_meme = db.query(MemeModel).filter(MemeModel.id == id).first()

    if db_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")

    # Delete the image from S3
    delete_image_from_s3(db_meme.image_url)

    db.delete(db_meme)
    db.commit()
    return db_meme