"""FinSight AI — Custom Exception Classes."""


class FinSightError(Exception):
    """Base exception for all FinSight AI errors."""
    pass


class ModelNotFoundError(FinSightError):
    """Raised when a required model artifact is not found on disk."""
    def __init__(self, model_path: str):
        super().__init__(f"Model artifact not found: {model_path}")
        self.model_path = model_path


class DataNotFoundError(FinSightError):
    """Raised when a required data file is not found."""
    def __init__(self, data_path: str):
        super().__init__(f"Data file not found: {data_path}")
        self.data_path = data_path


class PredictionError(FinSightError):
    """Raised when a model prediction fails."""
    pass


class AgentError(FinSightError):
    """Raised when the LangGraph agent encounters an error."""
    pass
