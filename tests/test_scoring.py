import pytest
from src.application.routers import get_score
from src.application.utils import TextPayload

# from fastapi.testclient import TestClient
# from src.main import app
# test = TestClient(app)


@pytest.mark.parametrize("text, result", [('Hello, world!', 0.0005),
                                          ('Fire and terrorism', 0.9997),
                                          ]
                         )
def test_check_scoring(text, result):
    payload = {
             "text": text
    }
    score = get_score(data=TextPayload(text=payload['text']))['data']['score']
    assert round(score.item(), 4) == result
