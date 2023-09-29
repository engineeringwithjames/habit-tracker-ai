from typing import Dict
from fastapi import FastAPI
from config import db

app = FastAPI()


@app.get("/")
async def main_route():
    user_ref = db.collection('users').document('user-0B_I5E_U8IgHvf7o').get()
    return {"message": user_ref.to_dict()}


@app.post("/query_llm_model")
async def query_llm_model(user_input: Dict[str, str]):
    return {"message": "Hey there "}


@app.post("/query_llm_model_with_context")
async def query_llm_model_with_context(user_input: Dict[str, str]):
    return {"message": "Hey there "}
