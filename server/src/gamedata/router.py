import json
import os
from typing import List

from fastapi import APIRouter, HTTPException
from src.database import db_session
from src.gamedata.models import GlyphItem
from src.gamedata.schemas import GlyphSchema

router = APIRouter()


@router.get("/test/")
async def read_users_me(db: db_session):
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


@router.post("/items/", response_model=List[GlyphSchema])
def add_items_from_file(glyphs: List[GlyphSchema], db: db_session):
    """
    Add GlyphItems to the database

    :param items: List of GlyphItemCreate Pydantic models.
    :param db: Database session dependency.
    :return: List of added GlyphItem objects.
    """
    added_items = []

    for item_data in glyphs:
        db_item = GlyphItem(**item_data.model_dump())
        db.add(db_item)
        added_items.append(db_item)

    return added_items
