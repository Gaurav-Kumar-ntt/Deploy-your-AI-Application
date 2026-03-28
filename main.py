from fastapi import FastAPI
from pydantic import BaseModel

from ai_pipeline import generate_response

app = FastAPI()


class PromptRequest(BaseModel):
    prompt: str


@app.get("/")
def home():
    return {"message": "AI API is running"}


@app.post("/generate")
def generate(request: PromptRequest):

    response = generate_response(request.prompt)

    return {
        "prompt": request.prompt,
        "response": response
    }