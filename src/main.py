"""API module with infra endpoints."""
import torch

from inference.data_processors.processor import Processor
from fastapi import FastAPI
from nlpiper.core import Document
from pydantic import BaseModel
from starlette.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT
)
from typing import Dict

from src.logger import get_logger, ENV
from src.utils import (
    get_model,
    get_preprocessing,
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
preprocessing = get_preprocessing()


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
    log.info(f"Received request: {news}")

    # Apply preprocessing
    processor = Processor(preprocessing=preprocessing)
    doc = processor.preprocess(Document(news.text))

    # Model inference
    with torch.no_grad():
        offsets = torch.zeros(1, dtype=torch.long)
        inference = model(doc.output, offsets)

    # Postprocessing
    predicted_class = inference.argmax(1).item() + 1
    news_classification = NEWS_CLASSIFICATION[predicted_class]
    confidence = round(inference.softmax(1).max().item(), 4) * 100

    log.info(f"Predicted class: {news_classification}")
    log.info(f"Confidence: {confidence}")

    return {
        "classification": news_classification,
        "confidence": confidence
    }


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
