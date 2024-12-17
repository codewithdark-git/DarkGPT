from sqlalchemy import Column, Integer, String
from app.database import Base

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    embedding = Column(String)

    def __repr__(self):
        return f"<Document(title={self.title}, id={self.id})>"
