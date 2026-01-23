"""FastAPI RAG Application"""
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "RAG API - See README.md for full implementation"}
