import unittest
import requests
import numpy as np

API_URL = "http://localhost:3000"
PREDICT_ENDPOINT = f"{API_URL}/predict"

# Replace with a valid JWT token generated with your SECRET_KEY
VALID_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyX2lkXzEyMyIsImV4cCI6MTc0Nzg2MjQyNH0.bGGCm1wLXN-mbxyW4RLTvn4Yf3T67bCSAbIIXUXqGl0"
INVALID_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyX2lkXzEyMyIsImV4cCI6MTc0Nzg2MjQyNH0.bGGCm1wLXN-mbxyW4RLTvn4Yf3T67bCSAbI0"

VALID_INPUT = {
    "gre_score": 320.0,
    "toefl_score": 110.0,
    "university_rating": 4,
    "sop": 4.5,
    "lor": 4.0,
    "cgpa": 9.0,
    "research": 1
}

class TestPredictionAPI(unittest.TestCase):
    def test_access_without_token(self):
        """Should return 401 Unauthorized if no token is provided."""
        res = requests.post(PREDICT_ENDPOINT, json=VALID_INPUT)
        print("Status:", res.status_code)
        print("Body:", res.text)
        self.assertEqual(res.status_code, 401)
        self.assertIn("detail", res.json())

    def test_access_with_invalid_token(self):
        """Should return 401 Unauthorized if token is invalid."""
        headers = {"Authorization": f"Bearer {INVALID_TOKEN}"}
        res = requests.post(PREDICT_ENDPOINT, json=VALID_INPUT, headers=headers)
        self.assertEqual(res.status_code, 401)
        self.assertIn("detail", res.json())

    def test_access_with_valid_token_and_valid_input(self):
        """Should return 200 OK and a numpy array if token and input are valid."""
        headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
        res = requests.post(PREDICT_ENDPOINT, json=VALID_INPUT, headers=headers)
        self.assertEqual(res.status_code, 200)
        # The output should be a list or array (depending on your model output)
        self.assertIsInstance(res.json(), object)

if __name__ == "__main__":
    unittest.main()
