from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Define a self-referential relationship for subtasks
    parent_id = Column(Integer, ForeignKey("tasks.id"))
    subtasks = relationship("Task", remote_side=[id], foreign_keys=[parent_id])
