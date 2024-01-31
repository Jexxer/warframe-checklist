from .Item import ItemSchema


class GlyphSchema(ItemSchema):
    description: str | None = None
    imageName: str | None = None
    masterable: bool | None = None
    excludeFromCodex: bool | None = None
