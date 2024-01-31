from sqlalchemy import Boolean, Column, Integer, String
from src.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    name = Column(String, nullable=False)
    tradable = Column(Boolean, nullable=False)
    uniqueName = Column(String, nullable=False)

    # Polymorphic configuration using 'category' as the discriminator
    __mapper_args__ = {
        "polymorphic_identity": "item",
        "polymorphic_on": 'category',
    }