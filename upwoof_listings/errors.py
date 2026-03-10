class ClientError(Exception):
    def __init__(self, response=None):
        self.response = response
        super().__init__(f"Client error: {response.status_code if response else 'Unknown'}")

class ResourceNotFoundError(ClientError):
    def __init__(self, response=None):
        super().__init__(response)
        self.message = "Resource not found"
