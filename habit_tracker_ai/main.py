import os
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from typing import Dict
from fastapi import FastAPI
from dotenv import load_dotenv
from agents.habit_lookup_agent import lookup_habit
from models.UserQuery import UserQuery

load_dotenv()

app = FastAPI()


@app.get("/")
async def main_route():
    return {"message": "user_ref.to_dict()"}


@app.post("/query_llm_model/")
async def query_llm_model(userQuery: UserQuery):
    list_of_habits = lookup_habit(userQuery.user_id)

    template = """
        given the user's existing habits {list_of_habits}
        and their goal of {user_goal}. 
        generate 5 habits similar in words that would
        meet their goal and remove any habit you generate that 
        already exists in their list of habits.
        If there are no existing habits then just generate 5 habits
        that would meet their goal.
        Your answer should only contain 5 habits in a
        string separated by a comma.
        An example of a valid answer is:
        "go to the gym, eat healthy, read a book, meditate,
        and go for a walk"
    """

    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",
    )

    prompt_template = PromptTemplate(
        template=template,
        input_variables=["list_of_habits", "user_goal"]
    )

    chain = LLMChain(
        llm=llm,
        prompt=prompt_template,
        verbose=True,
    )

    result = chain.run(
        list_of_habits=list_of_habits,
        user_goal=userQuery.information,
    )

    return {"message": result}


@app.post("/query_llm_model_with_context")
async def query_llm_model_with_context(user_input: Dict[str, str]):
    return {"message": "Hey there "}
