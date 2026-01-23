# Lesson 16: Deployment

## Theory

Deploying AI applications to production with FastAPI, Docker, and best practices.

### Components
1. **FastAPI**: REST API framework
2. **Docker**: Containerization
3. **Async**: Non-blocking operations
4. **Monitoring**: Logging and metrics
5. **Security**: Authentication, rate limiting

### FastAPI Example

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    text: str

@app.post("/query")
async def query(q: Query):
    result = await process_query(q.text)
    return {"result": result}
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0"]
```

## Challenge

Deploy a **Production RAG API** with authentication, rate limiting, and monitoring.

See `api.py`, `docker-compose.yml`, `Dockerfile`, `deploy.sh`, and `test_api.py` for examples.

## Resources
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Docker Docs](https://docs.docker.com/)
