from datetime import datetime
from sqlalchemy import func, Integer, Float, String
from typing_extensions import Annotated
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped



timestamp = Annotated[datetime, 
                      mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),]

class Base(DeclarativeBase):
    pass

class TempData(Base):

    __tablename__ = 'temp_data'

    index:Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    temperature:Mapped[float] = mapped_column(Float, nullable=False)
    temp_scales:Mapped[str] = mapped_column(String, nullable=False)
    creation_datetime:Mapped[timestamp]
