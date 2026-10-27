from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel, Field
from llm_code import analyze_code
import ast

app = FastAPI(
    title="AI CODE REVIEWER",
    description="Analyzes python code and suggests changes if bugs or syntax errors exist",
    version="1.0"
)

class CodeRequest(BaseModel):
    code: str = Field(min_length=1, max_length=10000)

@app.get("/")
def home():
    return {"message":"AI CODE REVIEWER is running"}

@app.post("/analyze")
def analyze(request: CodeRequest):
    try:
        ast.parse(request.code)
        return {"valid":True, "message":"No sytax errors found"}
    except SyntaxError as se:
        return {"valid":False, "error":se.msg, "line":se.lineno}

@app.post("/code_analyze")
def code_analyze(request: CodeRequest):
    try:
        response = analyze_code(request.code)
        return {
            "success": True,
            "response": response.model_dump()
        }
    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        print(f"LLM request failed: {exc}")

        raise HTTPException(
            status_code=502,
            detail=(
                "The LLM request failed. Check the API "
                "key, model availability, network, "
                "and provider usage limits."
            ),
        ) from exc