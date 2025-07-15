class SampleNotFoundError(Exception):
    def __init__(self):
        self.status_code = 404
        self.code = "S404"
        self.message = "Sample data not found"


class SampleAlreadyExistsError(Exception):
    def __init__(self):
        self.status_code = 409
        self.code = "S409"
        self.message = "Sample data already exists"
