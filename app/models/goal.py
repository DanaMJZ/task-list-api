from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import db
from typing import List
from .task import Task

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)

    # Wave6
    tasks: Mapped[List["Task"]] = relationship(back_populates="goal", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }

    @classmethod
    def from_dict(cls, data_dict):
        return cls(title=data_dict["title"])
