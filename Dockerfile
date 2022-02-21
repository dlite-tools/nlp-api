# Global default values for all stages
ARG homedir=/home/api
ARG poetry_version=1.1.11

######### BASE Image #########
FROM python:3.9-buster AS base

# For multi-stage, the ARG must be re-declared
ARG homedir
ARG poetry_version

ENV PATH="/poetry/bin:$PATH" \
    POETRY_VERSION=$poetry_version

RUN mkdir -p $homedir

WORKDIR $homedir

COPY poetry.lock pyproject.toml $homedir/

RUN curl -s https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py --output /install-poetry.py && \
    POETRY_HOME=/poetry python /install-poetry.py && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-root --no-dev && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/* /tmp/* /var/tmp/*

######### PRODUCTION Image #########
FROM python:3.9-slim-buster AS production

ARG homedir
ARG userid=1000
ARG username=api

ENV PATH="$homedir/.venv/bin:$PATH" \
    PYTHONPATH="$homedir:$homedir/.venv/lib/python3.9/site-packages/"

RUN groupadd --gid $userid $username && \
    useradd --home-dir $homedir --create-home --uid $userid --gid $userid --shell /bin/false --comment "Docker image user" --skel /dev/null $username

WORKDIR $homedir

EXPOSE 5000

COPY --from=base $homedir/.venv $homedir/.venv

COPY src $homedir/src

RUN chown -R $userid:$userid $homedir

USER $userid:$userid

CMD uvicorn src.main:app --log-level critical --host 0.0.0.0 --port 5000

######### TEST Image #########
FROM production AS tester

ARG homedir
ARG poetry_version

# Need root privileges to install dependencies
USER root

ENV CICD="TRUE" \
    PATH="/poetry/bin:$PATH" \
    POETRY_VERSION=$poetry_version

COPY poetry.lock pyproject.toml $homedir/

COPY --from=base /install-poetry.py /install-poetry.py

RUN libDeps='build-essential' && \
    apt-get update -y -qq > /dev/null && \
    apt-get -y -qq install $libDeps --no-install-recommends > /dev/null && \
    POETRY_HOME=/poetry python /install-poetry.py && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-root && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/* /tmp/* /var/tmp/*

COPY . $homedir/

CMD make tests
