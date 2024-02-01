import json
import os
from typing import List, Union

from fastapi import APIRouter, HTTPException
from src.database import db_session
from src.gamedata.models import GlyphItem
from src.gamedata.schemas import GlyphSchema

router = APIRouter()


@router.get("/test/")
async def test_endpoint(db: db_session):
    glyph_data = {
        "category": "Glyphs",
        "description": "A glyph depicting Equinox on a bright background.",
        "imageName": "equinox-glyph---bright.png",
        "masterable": False,
        "name": "Equinox Glyph - Bright",
        "tradable": False,
        "uniqueName": "/Lotus/Types/StoreItems/AvatarImages/ImageEquinoxBright",
    }

    glyph_item = GlyphItem(**glyph_data)

    # Add the GlyphItem to the session and commit the transaction
    db.add(glyph_item)
    db.commit()
    return {"message": "success"}

@router.post("/glyphs/", response_model=List[GlyphSchema])
def create_glyphs(glyphs: Union[GlyphSchema, List[GlyphSchema]], db: db_session):
    """
    Add GlyphItems to the database

    :param glyphs: GlyphSchema or List of GlyphSchema Pydantic models.
    :param db: Database session dependency.
    :return: List of added GlyphItem objects.
    """
    added_items = []

    # If glyphs is a single GlyphSchema, convert it to a list
    if isinstance(glyphs, GlyphSchema):
        glyphs = [glyphs]

    for item_data in glyphs:
        db_item = GlyphItem(**item_data.model_dump())
        db.add(db_item)
        added_items.append(db_item)

    return added_items

@router.get("/glyphs/", response_model=List[GlyphSchema])
def get_glyphs(db: db_session):
    """
    Get all GlyphItems from the database

    :param db: Database session dependency.
    :return: List of GlyphItem objects.
    """
    items = db.query(GlyphItem).all()
    return items

@router.get("/glyphs/{item_id}", response_model=GlyphSchema)
def get_glyph(item_id: int, db: db_session):
    """
    Get a GlyphItem from the database

    :param item_id: The ID of the item to retrieve.
    :param db: Database session dependency.
    :return: The GlyphItem object.
    """
    item = db.query(GlyphItem).get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item