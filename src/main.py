"""API module with infra endpoints."""
import torch
from typing import Dict

from fastapi import (
    FastAPI,
    HTTPException
)
from pydantic import BaseModel
from starlette.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_501_NOT_IMPLEMENTED
)

from src.logger import get_logger, ENV
from src.utils import (
    get_model,
    get_preprocessor,
    MODEL_OFFSETS,
    NEWS_CLASSIFICATION
)
from src.version import SERVICE_VERSION

log = get_logger(__name__)


class News(BaseModel):
    """News model."""
    text: str


class NewsClassification(BaseModel):
    """News classification model."""
    classification: str
    confidence: float


app = FastAPI(
    title="NLP API",
    description="Python API for NLP inference",
    version=SERVICE_VERSION
)

# Load machine learning model
model = get_model()

# Load preprocessing pipeline
preprocessor = get_preprocessor()


@app.post("/inference", response_model=NewsClassification, status_code=HTTP_200_OK)
async def inference(news: News):
    """Inference endpoint.

    Parameters
    ----------
    news : News
        News to be classified.

    Returns
    -------
    NewsClassification
        News classification result with confidence score.
    """
    raise HTTPException(
        status_code=HTTP_501_NOT_IMPLEMENTED,
        detail="Inference endpoint is not implemented yet."
    )


@app.get("/", status_code=HTTP_200_OK)
async def root() -> Dict:
    """Root API path.

    Returns
    -------
    dict
        Returns service environment and version
    """
    log.info("Get request at /")
    return {
        "version": SERVICE_VERSION,
        "environment": ENV
    }


@app.get("/health", status_code=HTTP_204_NO_CONTENT)
async def health() -> None:
    """K8s endpoint to check if the application is up and running."""
    log.info("Get request at /health")
    return None


@app.get("/ready", status_code=HTTP_204_NO_CONTENT)
async def ready() -> None:
    """K8s endpoint to check if the application is ready to serve requests."""
    log.info("Get request at /ready")
    return None
