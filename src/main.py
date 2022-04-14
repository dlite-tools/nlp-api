"""API module with infra endpoints."""
from typing import Dict

from fastapi import FastAPI
from starlette.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT
)

from src.logger import get_logger, ENV
from src.version import SERVICE_VERSION

log = get_logger(__name__)

app = FastAPI(
    title="NLP API",
    description="Python API for NLP inference",
    version=SERVICE_VERSION,
    redoc_url=None,
    docs_url="/docs"
)


@app.post("/inference", status_code=HTTP_200_OK)
async def inference(payload: Dict):
    """
    NLP inference endpoint.

    :param payload:
    :return:
    """
    log.info(f"Received request: {payload}")
    return {"message": "OK"}


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
