from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    from models.user import User
    from services.user_service import UserService
    from schemas.user_schema import UserSchemaPayload
    
    Base.metadata.create_all(bind=engine)
    
    service = UserService()

    db = SessionLocal()
    try:
        root_user = db.query(User).filter(User.username == "root").first()
        if not root_user:
            root_user_payload  = UserSchemaPayload(username="root", password="root")
            service.create(db, root_user_payload)
            print("Usuário root criado com sucesso.")
        else:
            print("Usuário root já existe.")
    finally:
        db.close()
