"""
Lesson 16: Production FastAPI RAG Application

Complete production-ready API with authentication, rate limiting, and monitoring.
"""

from fastapi import FastAPI, HTTPException, Depends, Security, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import time
from collections import defaultdict
from datetime import datetime, timedelta
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="RAG API",
    description="Production RAG API with authentication and rate limiting",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Authentication
# ============================================================================

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

# In production, store in database or environment variable
VALID_API_KEYS = {
    "test-key-123": {"user": "test_user", "tier": "free"},
    "prod-key-456": {"user": "prod_user", "tier": "premium"}
}


async def verify_api_key(api_key: str = Security(API_KEY_HEADER)):
    """Verify API key"""
    if api_key not in VALID_API_KEYS:
        logger.warning(f"Invalid API key attempt: {api_key[:10]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return VALID_API_KEYS[api_key]


# ============================================================================
# Rate Limiting
# ============================================================================

class RateLimiter:
    """Simple in-memory rate limiter"""
    def __init__(self):
        self.requests = defaultdict(list)
        self.limits = {
            "free": {"requests": 10, "window": 60},  # 10 req/min
            "premium": {"requests": 100, "window": 60}  # 100 req/min
        }
    
    def check_rate_limit(self, user: str, tier: str) -> bool:
        """Check if user is within rate limit"""
        now = datetime.now()
        limit_config = self.limits.get(tier, self.limits["free"])
        
        # Remove old requests
        cutoff = now - timedelta(seconds=limit_config["window"])
        self.requests[user] = [
            req_time for req_time in self.requests[user]
            if req_time > cutoff
        ]
        
        # Check limit
        if len(self.requests[user]) >= limit_config["requests"]:
            return False
        
        # Add current request
        self.requests[user].append(now)
        return True


rate_limiter = RateLimiter()


async def check_rate_limit(user_info: dict = Depends(verify_api_key)):
    """Check rate limit for user"""
    user = user_info["user"]
    tier = user_info["tier"]
    
    if not rate_limiter.check_rate_limit(user, tier):
        logger.warning(f"Rate limit exceeded for user: {user}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )
    return user_info


# ============================================================================
# Models
# ============================================================================

class QueryRequest(BaseModel):
    """Query request model"""
    query: str = Field(..., min_length=1, max_length=500)
    max_results: Optional[int] = Field(default=5, ge=1, le=20)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is machine learning?",
                "max_results": 5
            }
        }


class QueryResponse(BaseModel):
    """Query response model"""
    query: str
    answer: str
    sources: List[str]
    processing_time: float


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    version: str


class MetricsResponse(BaseModel):
    """Metrics response"""
    total_requests: int
    avg_response_time: float
    error_rate: float


# ============================================================================
# Metrics
# ============================================================================

class Metrics:
    """Simple metrics tracker"""
    def __init__(self):
        self.total_requests = 0
        self.total_errors = 0
        self.response_times = []
    
    def record_request(self, duration: float, error: bool = False):
        """Record request metrics"""
        self.total_requests += 1
        if error:
            self.total_errors += 1
        self.response_times.append(duration)
        
        # Keep only last 1000
        if len(self.response_times) > 1000:
            self.response_times = self.response_times[-1000:]
    
    def get_metrics(self) -> dict:
        """Get current metrics"""
        return {
            "total_requests": self.total_requests,
            "avg_response_time": sum(self.response_times) / len(self.response_times) if self.response_times else 0,
            "error_rate": self.total_errors / self.total_requests if self.total_requests > 0 else 0
        }


metrics = Metrics()


# ============================================================================
# Endpoints
# ============================================================================

@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": "RAG API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics(user_info: dict = Depends(verify_api_key)):
    """Get API metrics (authenticated)"""
    logger.info(f"Metrics requested by {user_info['user']}")
    return MetricsResponse(**metrics.get_metrics())


@app.post("/query", response_model=QueryResponse)
async def query(
    request: QueryRequest,
    user_info: dict = Depends(check_rate_limit)
):
    """
    Query the RAG system.
    
    Requires authentication and is rate-limited.
    """
    start_time = time.time()
    
    try:
        logger.info(f"Query from {user_info['user']}: {request.query}")
        
        # Simulate RAG processing
        # In production, this would call your actual RAG system
        answer = f"Answer to '{request.query}': This is a simulated response. " \
                 f"In production, this would query your vector database and LLM."
        
        sources = [
            "document1.pdf (page 5)",
            "document2.pdf (page 12)",
            "document3.pdf (page 3)"
        ][:request.max_results]
        
        processing_time = time.time() - start_time
        
        # Record metrics
        metrics.record_request(processing_time, error=False)
        
        logger.info(f"Query completed in {processing_time:.2f}s")
        
        return QueryResponse(
            query=request.query,
            answer=answer,
            sources=sources,
            processing_time=processing_time
        )
        
    except Exception as e:
        processing_time = time.time() - start_time
        metrics.record_request(processing_time, error=True)
        logger.error(f"Query error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# Startup/Shutdown
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Run on startup"""
    logger.info("Starting RAG API...")
    logger.info("API is ready to accept requests")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on shutdown"""
    logger.info("Shutting down RAG API...")


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
