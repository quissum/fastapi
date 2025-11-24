from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

from app.db.session import Model


class MUser(SQLAlchemyBaseUserTableUUID, Model):
    __tablename__ = "users"
