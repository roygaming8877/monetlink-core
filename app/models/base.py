import uuid
from datetime import datetime
from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

class MonetLinkBaseModel(DeclarativeBase):
    """
    Enterprise Abstract Base Class for all MonetLink Database Models.
    Enforces UUIDs for primary keys to prevent ID enumeration attacks and 
    automates timestamp management at the database level.
    """
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4()), 
        index=True,
        doc="Universally Unique Identifier for the record."
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False,
        doc="Exact timestamp of record creation. Handled by Postgres server_default."
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False,
        doc="Timestamp automatically updated on row modification."
    )
    
