from fastapi import APIRouter
from src.application.utils import ScoreResponse, TextPayload, Preparation, request_id, nlp, model, tokenizer, SPACE_DIMESION

router = APIRouter()


@router.post("/disaster_prediction",
             response_model=ScoreResponse,
             description="""return prediction score"""
             )
def get_score(data: TextPayload):
    text = Preparation.pipeline(data.text, nlp)
    text = tokenizer(text,
                     padding='max_length',
                     max_length=SPACE_DIMESION,
                     truncation=True,
                     return_tensors='pt',
                     return_attention_mask=True,
                     return_token_type_ids=True)
    print(text)
    score = model(**text)[0][1]

    return {
        "requestId": request_id.get(),
        "data": {
            "score": score
        }
    }


@router.get("/",
            description="""return information"""
            )
def get_docs():
    return {
        "requestId": request_id.get(),
        "information": "scoring of disaster tweets!"
    }
