import os
import sys

# Add the backend directory to sys.path so we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_scaling_advice():
    print("Sending request to /validate/scaling-advice...")
    response = client.post(
        "/validate/scaling-advice",
        json={
            "idea_text": "A B2B SaaS platform for automated invoice processing",
            "revenue_context": "₹40L ARR, growing 10% MoM"
        }
    )
    
    if response.status_code == 200:
        print("Success! Response JSON:")
        print(response.json())
    else:
        print(f"Error {response.status_code}:")
        print(response.text)

if __name__ == "__main__":
    test_scaling_advice()
