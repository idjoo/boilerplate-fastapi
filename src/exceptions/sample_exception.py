class SampleError(Exception):
    def __init__(
        self,
        message: str = "Internal Server Error",
        status_code: int = 500,
    ):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)


class SampleNotFoundError(SampleError):
    def __init__(self):
        super().__init__(status_code=404, message="Sample Not Found")


class SampleAlreadyExistsError(SampleError):
    def __init__(self):
        super().__init__(status_code=409, message="Sample Already Exists")
