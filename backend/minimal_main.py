from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class TestRequest(BaseModel):
    text: str

@app.post("/test")
async def test_endpoint(request: TestRequest):
    return {"message": "Test successful", "input": request.text}
