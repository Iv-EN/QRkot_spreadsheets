from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer
from sqlalchemy.sql import func

from app.core.db import Base


class BaseModel(Base):
    """Базовая модель."""

    __abstract__ = True
    __table_args__ = (
        CheckConstraint("full_amount > 0"),
        CheckConstraint("invested_amount >= 0"),
        CheckConstraint("invested_amount <= full_amount"),
    )

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=func.now())
    close_date = Column(DateTime)
