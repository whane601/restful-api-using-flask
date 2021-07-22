from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.user import Base as base


class DBConnector():
    def __init__(self, db_uri: str) -> None:
        engine = create_engine(db_uri)
        session = sessionmaker(bind=engine)
        self._session = session()

        base.metadata.create_all(engine)

    def session(self):
        return self._session
