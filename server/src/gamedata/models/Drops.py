from sqlalchemy import Column, Float, Integer, String
from src.database import Base


class Drop(Base):
    __tablename__ = 'drops'
    
    id = Column(Integer, primary_key=True)
    chance = Column(Float, nullable=False)
    location = Column(String, nullable=False)
    rarity = Column(String, nullable=False)
    type = Column(String, nullable=False)