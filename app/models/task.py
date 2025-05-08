from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.db import db
from datetime import datetime


# Wave1
class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    # Wave6
    goal_id: Mapped[int | None] = mapped_column(ForeignKey("goal.id"), nullable=True)
    goal: Mapped["Goal"] = relationship(back_populates="tasks")

    def to_dict(self):
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }
        if self.goal_id is not None:
            task_dict["goal_id"] = self.goal_id
        return task_dict
    
    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title=data_dict["title"],
            description=data_dict["description"]
        )
# Wave4
    @property
    def is_complete(self):
        return self.completed_at is not None