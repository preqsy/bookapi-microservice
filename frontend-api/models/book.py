from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, TIMESTAMP, text
from sqlalchemy.orm import relationship

from core.db import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False, unique=True)
    page_count = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    published_date = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    status = Column(Boolean, nullable=False, server_default="TRUE")
    categories = Column(String, nullable=False)
    is_deleted = Column(Boolean, nullable=False, server_default="FALSE")
    owner = relationship("Users")
