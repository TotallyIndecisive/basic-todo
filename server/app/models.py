from sqlalchemy import Column, Integer, String

from app.database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True, nullable=False)
