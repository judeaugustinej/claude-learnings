import requests as req
from embedding import vector_embedding

expected_string = "As students at the United States Navy's elite fighter weapons school compete to be best in the class, one daring young pilot learns a few things from a civilian instructor that are not taught in the classroom."


class MockResponse:
    """
    Mock class for requests.Response
    """

    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise req.HTTPError(
                f"HTTP request failed with status code {self.status_code}",
                response=self,
            )


class requests:
    """
    Mock class for requests module to simulate a post request to the OpenAI API.
    """

    # Retrieve the embedding from the vector_embedding dictionary
    embedding = vector_embedding.get("data").get("embedding")

    # Mock response data based on (https://platform.openai.com/docs/api-reference/embeddings/create)
    _mock_response_data = {
        "object": "list",
        "data": [
            {
                "object": "embedding",
                "embedding": embedding,
                "index": 0,
            }
        ],
        "model": "text-embedding-ada-002",
        "usage": {"prompt_tokens": 2, "total_tokens": 2},
    }

    @staticmethod
    def post(endpoint, json, headers):
        """
        Mock method for the requests.get() method.
        """
        if "Authorization" not in headers:
            raise req.exceptions.MissingSchema("Missing Authorization header")

        if not endpoint.startswith("https:"):
            raise req.exceptions.MissingSchema("Invalid endpoint")

        print("Mocking request to:", endpoint)
        if json is None:
            json = {}

        query_str = json["input"]
        mocked_response_data = requests._mock_response_data

        # Mock the behavior of the server
        if query_str != expected_string:
            return MockResponse(None, 404)
        elif query_str == "error":
            return MockResponse(None, 500)
        else:
            # Return the embedding for the "action movies" query
            return MockResponse([mocked_response_data], 200)
