Step 1 — Install Required Libraries

Install FastAPI and the ASGI server.

pip install fastapi uvicorn requests python-dotenv


These libraries allow you to:

build an API server

run the application locally

connect to the LLM API

Step 2 — Create the AI Pipeline

Create a file called:

ai_pipeline.py


This file will contain your AI logic.

Add the following code.

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
API_URL = os.getenv("LLM_API_URL")
MODEL = os.getenv("LLM_MODEL")


def generate_response(prompt):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    data = response.json()

    return data["choices"][0]["message"]["content"]


This module connects to the LLM and returns a generated response.

Step 3 — Create the FastAPI Server

Create the main application file:

main.py


Add the following code.

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


This code creates two API endpoints.

Step 4 — Start the API Server

Run the server using:

uvicorn main:app --reload


You should see output like:

Uvicorn running on http://127.0.0.1:8000


Step 5 — Test the API

Open your browser and visit:

http://127.0.0.1:8000


You should see:

{"message": "AI API is running"}


Step 6 — Use the API Documentation

FastAPI automatically generates API documentation.

Open:

http://127.0.0.1:8000/docs


You will see an interactive interface where you can test your API.

Step 7 — Test the Generate Endpoint

Inside the documentation page:

Open the /generate endpoint

Click Try it out

Enter a prompt

Example request:

{
  "prompt": "Explain what an AI agent is."
}


Example response:

{
  "prompt": "Explain what an AI agent is.",
  "response": "An AI agent is a system that can perceive its environment..."
}


Your AI system is now accessible through an API.

How the Deployment Works

Your application now follows this architecture.

1. API Request

A client sends a request to the endpoint.

Example:

POST /generate


2. AI Pipeline Execution

The API sends the prompt to the AI pipeline.

3. LLM Response

The pipeline calls the LLM API and generates a response.

4. API Response

The result is returned as JSON.
