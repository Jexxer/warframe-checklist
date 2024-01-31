from datetime import datetime, timedelta
from enum import Enum as PyEnum

import pytz
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text, Time
from sqlalchemy.orm import relationship
from src.database import Base


class ResetInterval(PyEnum):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    BIWEEKLY_FRIDAY = 'biweekly_friday'  # Custom reset interval for Baro Ki'Teer

class TaskEventType(PyEnum):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    SPECIAL_EVENT = 'special_event'

class TaskVisibility(PyEnum):
    GLOBAL = 'global'
    USER_CREATED = 'user_created'

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Define a self-referential relationship for subtasks
    parent_id = Column(Integer, ForeignKey("tasks.id"))
    subtasks = relationship("Task", remote_side=[id], foreign_keys=[parent_id])

    # New columns for expiration, reset, and reset interval
    expiration_date = Column(DateTime(timezone=True), nullable=True)
    reset_interval = Column(Enum(ResetInterval), default=ResetInterval.DAILY, nullable=False)

    # New column for a specific reset time (time-only, date-unaware)
    reset_time = Column(Time(timezone=True), nullable=True)

    # Additional fields
    difficulty = Column(String, nullable=True)  # Difficulty level
    location_planet = Column(String, nullable=True)  # Planet where the task/event takes place
    location_city = Column(String, nullable=True)  # City or specific location within the game
    start_date = Column(DateTime(timezone=True), nullable=True)  # Start date and time
    end_date = Column(DateTime(timezone=True), nullable=True)  # End date and time
    event_type = Column(Enum(TaskEventType), nullable=True)  # Type of event (e.g., daily, weekly)
    additional_notes = Column(Text, nullable=True)  # Additional information or notes
    icon_url = Column(String, nullable=True)  # URL to an icon or image representing the task/event
    visibility = Column(Enum(TaskVisibility), default=TaskVisibility.GLOBAL, nullable=False)  # Task visibility

    def is_expired(self):
        current_time = datetime.now(pytz.utc)
        if self.reset_time:
            current_date = current_time.date()
            reset_datetime = datetime.combine(current_date, self.reset_time)
            if current_time >= reset_datetime:
                return True
        elif self.expiration_date:
            return current_time >= self.expiration_date
        return False

    def reset_task(self):
        current_time = datetime.now(pytz.utc)

        if self.reset_interval == ResetInterval.DAILY:
            if self.reset_time:
                current_date = current_time.date()
                next_reset_datetime = datetime.combine(current_date, self.reset_time) + timedelta(days=1)
                self.reset_time = next_reset_datetime.time()

                # Calculate and set the expiration date (24 hours from the reset time)
                self.expiration_date = next_reset_datetime + timedelta(hours=24)
        elif self.reset_interval == ResetInterval.WEEKLY:
            if self.reset_time:
                current_date = current_time.date()
                next_reset_datetime = datetime.combine(current_date, self.reset_time) + timedelta(weeks=1)
                self.reset_time = next_reset_datetime.time()

                # Calculate and set the expiration date (7 days from the reset time)
                self.expiration_date = next_reset_datetime + timedelta(days=7)
        elif self.reset_interval == ResetInterval.BIWEEKLY_FRIDAY:
            if self.reset_time:
                current_date = current_time.date()
                current_weekday = current_date.weekday()
                days_until_friday = (4 - current_weekday + 7) % 7  # Calculate days until the next Friday
                next_reset_datetime = datetime.combine(current_date, self.reset_time) + timedelta(days=days_until_friday)
                next_reset_datetime += timedelta(weeks=2)  # Move to the next biweekly interval
                self.reset_time = next_reset_datetime.time()

                # Calculate and set the expiration date (48 hours from the reset time)
                self.expiration_date = next_reset_datetime + timedelta(hours=48)
