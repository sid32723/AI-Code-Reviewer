from typing import Literal
from pydantic import BaseModel, Field

class CodeIssue(BaseModel):
    title: str = Field(description="A short title describing the issue")
    severity: Literal["HIGH", "MEDIUM", "LOW"] = Field(description="Severity of the issue")
    explanation: str = Field(description="Explanation of why the issue could have occured")
    suggested_fix: str = Field(description="A change of code that could fix the issue")
    test_cases: str = Field(description="A sample test case to test the suggested fix")

class CodeReview(BaseModel):
    summary: str = Field(description="Brief overall summary of the code review")
    issues: list[CodeIssue] = Field(description="List of potential issues found; empty if none")