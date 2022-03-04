# Model Deployment

We have built a machine learning model, but we need to make it available to use it.
Let's build an API to serve the model.

For the API, we will be using [FastAPI framework](https://fastapi.tiangolo.com)

There are several ways to deploy the model, each with its pros and cons.
None of them is better than the other. It is essential to understand your requirements and choose the one that fits your problem.
Don't feel ashamed for picking a simpler solution, and also, don't try to go straight to the most complex solution if you're not at the stage of your project for that implementation.

When it comes to deploying the model, we have two major approaches:

- Download the model files when the server starts up
- Create a layer with the model files inside the container

## Download model

The approach here is to have the model server, when it starts up, download the model weights from somewhere specified by an environment variable.

This approach adds some complexity because we add the model registry as an infrastructure dependency that needs to be up so that everything does not break.

On the other hand, the benefit of downloading the model weights is that we end up with fewer container images. We only need a generic container image with the proper dependencies to run the server and the model. We can reuse this with multiple versions of the model by changing only the environment variable with the information of where the model should de downloaded.

The place where the model is stored is also crucial in the process. A simple solution is to store the model in an AWS S3 bucket, and then the model server downloads it when it starts up. Whenever you want to deploy a new version, you only need to upload and restart the application containers. This process has some flaws that can become dangerous. One of them is that it is harder to keep the running model version traceability.

What we need is a centralized tracking system for trained machine learning models, known as a **model registry**. A model registry is a system that stores model lineage, versioning, and other configuration information. There is popular open source registry built by [MLFlow](https://www.mlflow.org/docs/latest/model-registry.html).

## Model into container

In this approach, we create a layer with the model files inside the application's container. With this approach, infrastructure dependency doesn't become part of the production system.
We can still serve inferences even if our MLFlow instance is unavailable.

When storing the model weights into a container, the simplest solution is to store them in the app's repository.
This solution is only viable if the file sizes are not too large. In this way, we have the traceability of the deployed models.

The alternative is to store the model in a model registry and download it during the docker image build.
