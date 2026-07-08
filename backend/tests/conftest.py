import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.database import Base, get_db
from app.main import app

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        "sqlite:///:memory:", 
        connect_args={"check_same_thread": False}, 
        poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture
def db(engine):
    connection = engine.connect()
    transaction = connection.begin()

    SessionLocal = sessionmaker(bind=connection, autocommit=False)
    session = SessionLocal()
    session.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture(scope="session")
def admin_token(engine):
    from app.models import User
    from app.core.security import hash_password, create_access_token
    from sqlalchemy.orm import sessionmaker

    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    admin = User(
        email="admin@test.com", 
        hashed_password=hash_password('testtest'), 
        role="admin"
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)

    token = create_access_token({"user_id": admin.id})
    db.close()
    return token

@pytest.fixture(scope="session")
def operator_token(engine):
    from app.models import User
    from app.core.security import hash_password, create_access_token
    from sqlalchemy.orm import sessionmaker

    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    operator = User(
        email="operator@test.com", 
        hashed_password=hash_password("testtest"),
        role="operator"
    )
    db.add(operator)
    db.commit()
    db.refresh(operator)

    token = create_access_token({"user_id": operator.id})
    db.close()
    return token

@pytest.fixture(scope="session")
def viewer_token(engine):
    from app.models import User
    from app.core.security import hash_password, create_access_token
    from sqlalchemy.orm import sessionmaker

    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    viewer = User(
        email="viewer@test.com", 
        hashed_password=hash_password("testtest"),
        role="viewer"
    )
    db.add(viewer)
    db.commit()
    db.refresh(viewer)

    token = create_access_token({"user_id": viewer.id})
    db.close()
    return token

@pytest.fixture(autouse=True)
def disable_audit_middleware(db):
    """讓audit middleware使用測試db而不是正式db"""
    with patch("app.middleware.audit.SessionLocal", return_value=db):
        yield