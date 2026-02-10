from typing import List, Optional

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from freeflow_llm import FreeFlowClient, NoProvidersAvailableError


class ChatMessage(BaseModel):
  role: str
  content: str


class ChatRequest(BaseModel):
  messages: List[ChatMessage]
  temperature: Optional[float] = 0.3
  maxTokens: Optional[int] = 600


class ChatResponse(BaseModel):
  reply: str


app = FastAPI(title="FreeFlow LLM bridge")


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
  if not request.messages:
    raise HTTPException(status_code=400, detail="messages must not be empty")

  ff_messages = [
    {"role": msg.role, "content": msg.content} for msg in request.messages
  ]

  try:
    with FreeFlowClient() as client:
      response = client.chat(
        messages=ff_messages,
        temperature=request.temperature,
        max_tokens=request.maxTokens,
      )
  except NoProvidersAvailableError as exc:
    raise HTTPException(
      status_code=503,
      detail=f"No FreeFlow providers available: {exc}",
    ) from exc
  except Exception as exc:  # noqa: BLE001
    raise HTTPException(
      status_code=500,
      detail="FreeFlow service error",
    ) from exc

  return ChatResponse(reply=response.content)

