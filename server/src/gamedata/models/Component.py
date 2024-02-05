from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base


class Component(Base):
    __tablename__ = 'components'

    id = Column(Integer, primary_key=True)
    uniqueName = Column(String, nullable=False)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    itemCount = Column(Integer, nullable=True)
    imageName = Column(String, nullable=True)
    tradable = Column(Boolean, nullable=True)
    masterable = Column(Boolean, nullable=True)
    drops = relationship('Drop')