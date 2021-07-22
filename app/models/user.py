from typing import Any
from typing import Dict
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50))
    job_title = Column(String(50))
    email = Column(String(50))
    mobile = Column(String(50))
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, nullable=True, onupdate=func.now())

    def serialize(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "job_title": self.job_title,
            "communicate_information": {
                "email": self.email,
                "mobile": self.mobile,
            }
        }
