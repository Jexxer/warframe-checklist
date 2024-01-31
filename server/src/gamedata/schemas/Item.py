from pydantic import BaseModel


class ItemSchema(BaseModel):
    id: int | None = None
    category: str
    name: str
    tradable: bool
    uniqueName: str
    
    class Config:
        from_attributes = True
