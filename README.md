# Serving Machine Learning Models

When serving machine learning models, data preparation and model training are just two factors to consider. This repository explores how to serve a machine learning (ML) model using a Rest API.

To know more about model training, please check the [machine learning model training proposed solution](https://github.com/dlite-tools/nlp-training).

The objective of this repository is to propose an approach serve a machine learning model using a Rest API built with [FastAPI] and using a inference package created in [model training proposed solution](https://github.com/dlite-tools/nlp-training). This way we ensure that the data transformation is done the same way as the training process.

# Architecture

[Add diagram]

- Include nlp-training repository exportig a inference package.
- Include a Rest API built with [FastAPI]
- Inference package is used to transform the input data. (dependency)
- The Rest API is used to serve the inference package.


# Project Setup

The backbone of our REST API will be:
- [FastAPI](https://fastapi.tiangolo.com/) - lets you easily set up a REST API.
- [Uvicorn](https://www.uvicorn.org/) - server that lets you do async programming with Python.
- [Pydantic](https://pydantic-docs.helpmanual.io/) - data validation by introducing types for our request and response data.

Some tools will help us write some better code:

- [flake8](https://flake8.pycqa.org/en/latest/) - check for code style (PEP 8) compliance
- [mypy](https://mypy.readthedocs.io/en/stable/) - check for type annotations
- [pydocstyle](http://www.pydocstyle.org/en/stable/) - check for docstring style compliance
