class AppError(Exception):
    status_code = 500

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class ResourceConflictError(AppError):
    status_code = 409


class ResourceNotFoundError(AppError):
    status_code = 404


class FeatureNotImplementedError(AppError):
    status_code = 501
