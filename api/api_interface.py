from fastapi import FastAPI, HTTPException, Request, Security, status
from pydantic import BaseModel as PydanticBaseModel
from classification import Classification
from fastapi.security import APIKeyHeader
import os


api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)
API_KEY_MY_SERVER = os.getenv("API_KEY_MY_SERVER")

def get_api_key(
    api_key_header: str = Security(api_key_header),
) -> str:
    if api_key_header == API_KEY_MY_SERVER:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


app = FastAPI()
model = Classification()


class EmailContent(PydanticBaseModel):
    email_content: str

@app.post("/process_email")
def process_email(email: EmailContent,api_key: str = Security(get_api_key)):
    print( Security(get_api_key))
    try:
        result = model.process_email(email.email_content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/private")
def private(api_key: str = Security(get_api_key)):
    """A private endpoint that requires a valid API key to be provided."""
    return f"Private Endpoint. API Key: {api_key}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
