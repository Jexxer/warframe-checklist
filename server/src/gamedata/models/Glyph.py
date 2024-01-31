from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from ..utils import Category
from .Item import Item


class GlyphItem(Item):
    __tablename__ = 'glyph_items'
    id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    description = Column(String, nullable=False)
    imageName = Column(String, nullable=False)
    masterable = Column(Boolean, nullable=False)
    excludeFromCodex = Column(Boolean, default=False)

    # Set the polymorphic_identity to match the category 'Glyphs'
    __mapper_args__ = {
        "polymorphic_identity": Category.Glyphs.value,
    }