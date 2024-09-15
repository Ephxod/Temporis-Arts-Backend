import pytest
import jwt
import httpx
from models.users import User
from models.records import Record
from models.musics import Music
from models.charts import Chart
from database.connection import get_session
from sqlalchemy import text
from config import SECRET_KEY
from main import app  
from datetime import datetime, timezone

@pytest.fixture(scope="session")
async def default_client():
    async with httpx.AsyncClient(app=app, base_url="https://app") as client:
        session = next(get_session())
        try:
            session.exec(text("DELETE FROM record"))
            session.exec(text("DELETE FROM chart"))
            session.exec(text("DELETE FROM music"))
            session.exec(text("DELETE FROM \"user\""))
            session.commit()

            sample_user = User(user_id="testid0", name="testname")
            session.add(sample_user)

            sample_music = Music(music_id=0, title="samplemusic0", composer="testcomposer")
            session.add(sample_music)
            session.commit()

            sample_chart = Chart(music_id=0, difficulty=0, level=1)
            sample_chart = Chart(music_id=0, difficulty=1, level=3)
            session.add(sample_chart)
            session.commit()

            sample_record = Record(user_id="testid0", music_id=0, difficulty=0, high_score=4567890, score_updated_date=datetime.now(timezone.utc))
            session.add(sample_record)
            session.commit()
            yield client  
        finally:
            session.exec(text("DELETE FROM record"))
            session.exec(text("DELETE FROM chart"))
            session.exec(text("DELETE FROM music"))
            session.exec(text("DELETE FROM \"user\""))
            session.commit()
            
@pytest.fixture(scope="session")
def create_test_jwt_token() -> str:
    payload = {
        "sub": "testjwtgenerate", 
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token
