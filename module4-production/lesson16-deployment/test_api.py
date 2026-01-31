"""
Lesson 16: API Tests

Test the production API endpoints.
"""

import requests
import time

BASE_URL = "http://localhost:8000"
API_KEY = "test-key-123"

def test_health():
    """Test health endpoint"""
    print("\n📋 Test 1: Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}")
    assert response.status_code == 200

def test_authentication():
    """Test authentication"""
    print("\n📋 Test 2: Authentication")
    
    # Without API key
    response = requests.post(f"{BASE_URL}/query", json={"query": "test"})
    print(f"  Without key: {response.status_code}")
    assert response.status_code == 403
    
    # With valid API key
    response = requests.post(
        f"{BASE_URL}/query",
        json={"query": "test"},
        headers={"X-API-Key": API_KEY}
    )
    print(f"  With key: {response.status_code}")
    assert response.status_code == 200

def test_query():
    """Test query endpoint"""
    print("\n📋 Test 3: Query Endpoint")
    response = requests.post(
        f"{BASE_URL}/query",
        json={"query": "What is machine learning?", "max_results": 3},
        headers={"X-API-Key": API_KEY}
    )
    print(f"  Status: {response.status_code}")
    data = response.json()
    print(f"  Answer length: {len(data['answer'])} chars")
    print(f"  Sources: {len(data['sources'])}")
    assert response.status_code == 200

def test_rate_limiting():
    """Test rate limiting"""
    print("\n📋 Test 4: Rate Limiting")
    
    # Make many requests
    success_count = 0
    rate_limited = False
    
    for i in range(15):
        response = requests.post(
            f"{BASE_URL}/query",
            json={"query": f"test {i}"},
            headers={"X-API-Key": API_KEY}
        )
        if response.status_code == 200:
            success_count += 1
        elif response.status_code == 429:
            rate_limited = True
            break
    
    print(f"  Successful requests: {success_count}")
    print(f"  Rate limited: {rate_limited}")
    assert rate_limited, "Rate limiting should trigger"

def test_metrics():
    """Test metrics endpoint"""
    print("\n📋 Test 5: Metrics")
    response = requests.get(
        f"{BASE_URL}/metrics",
        headers={"X-API-Key": API_KEY}
    )
    print(f"  Status: {response.status_code}")
    metrics = response.json()
    print(f"  Total requests: {metrics['total_requests']}")
    print(f"  Avg response time: {metrics['avg_response_time']:.3f}s")
    assert response.status_code == 200

def main():
    """Run all tests"""
    print("=" * 70)
    print("API Tests")
    print("=" * 70)
    print("\nMake sure the API is running: uvicorn api:app")
    
    try:
        test_health()
        test_authentication()
        test_query()
        test_rate_limiting()
        test_metrics()
        
        print("\n" + "=" * 70)
        print("✅ All tests passed!")
        print("=" * 70)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API")
        print("Make sure the API is running: uvicorn api:app")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
