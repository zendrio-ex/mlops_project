from pydantic import BaseModel
from transformers import BertTokenizer, BertModel
import spacy
import torch
import torch.nn as nn
import re

SPACE_DIMESION = 20

class ScoreResponse(BaseModel):
    class ScoreResponseData(BaseModel):
        score: float
    requestId: str
    data: ScoreResponseData


class TextPayload(BaseModel):

    text: str

    class Config:
        schema_extra = {
            "example": {
                "text": "Hello, world!"
            }
        }


class RequestId:
    def __init__(self):
        self.id: str = None

    def set(self, id: str):
        self.id = id

    def get(self):
        return self.id
    

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.bert = BertModel.from_pretrained("bert-base-uncased")  # embedding
        self.output_layer = nn.Sequential(
            nn.Linear(in_features=768, out_features=2),
            nn.Softmax(dim=1)
        )  # pooler_output returns 768 tensor size

    def forward(self, input_ids, attention_mask, token_type_ids):
        x = self.bert(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids).pooler_output
        x = self.output_layer(x)
        return x


class Preparation:
    
    @staticmethod
    def https_rem(text):
        return re.compile(r'https?://\S+').sub(r' https', text)

    @staticmethod
    def remove_punctuations(text: str) -> str:
        re_str = re.compile(r'\?|#|&|!|,|\.|"|"|\||\[|]|/|\||-|\+|\...|\d+|\*|:|@|\'|;|\)|\(')
        return re.sub(re_str, ' ', text)

    @staticmethod
    def lemmatization(text: str, nlp) -> str:
        text_ = nlp(text)
        return ' '.join([el.lemma_ for el in text_])
    
    @staticmethod
    def remove_multiple_spaces(text):
        return re.sub(' +', ' ', text)
    
    @staticmethod
    def pipeline(text, nlp):
        text = Preparation.remove_punctuations(Preparation.https_rem(text)).lower()
        text = Preparation.remove_multiple_spaces(Preparation.lemmatization(text, nlp))
        return text


request_id = RequestId()

nlp = spacy.load('en_core_web_sm')

model = Model()
model.load_state_dict(torch.load("./model/model.pth", map_location="cpu"))

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
