# BASE INSTALLATION
# =================

# Base on the heroku:18-build stack (ubuntu bionic) which has some helpers to compile libraries
# and install node and python ourselves
FROM heroku/heroku:18-build as build

MAINTAINER Tom Clark <tom@octue.com>

ENV PROJECT_ROOT=/app

ENV DEBIAN_FRONTEND=noninteractive


# NODE.JS RUNTIME ENVIRONMENT
# ===========================

# TODO unify as a multistage build with the node Dockerfile, so as to only copy over built
#  and minified assets to the production container (see the node dockerfile for a link to useful tutorial)
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - \
    && apt-get update -y && apt-get install -y --fix-missing --no-install-recommends nodejs


# PYTHON RUNTIME ENVIRONMENT
# ==========================
#
# Note: If compiling GDAL with python bindings, this needs to be done prior to the GDAL build.

ARG PYTHON_RUNTIME_VERSION=3.6.9

# Python installs for cpython
RUN apt-get update -y && apt-get install -y --fix-missing --no-install-recommends \
    git build-essential libbz2-dev libssl-dev libreadline-dev  libffi-dev libsqlite3-dev tk-dev

# Optional scientific package headers (useful for Numpy, Matplotlib, SciPy, etc)
RUN apt-get update -y && apt-get install libpng-dev libfreetype6-dev

# Run subsequent commands using bash, rather than the default bin/sh, which ensures that .bashrc is correctly sourced for users
# (see extensive discussion at https://stackoverflow.com/questions/20635472/using-the-run-instruction-in-a-dockerfile-with-source-does-not-work/39777387#39777387)
SHELL ["/bin/bash", "-c"]

# Install pyenv and add its shims and binaries to PATH
RUN curl https://pyenv.run | bash
ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

# Set C.UTF-8 locale for Python 3 interpreters. You can remove these for python 3.7 and later
# (see https://click.palletsprojects.com/en/7.x/python3/)
ENV LANG "C.UTF-8"
ENV LC_ALL "C.UTF-8"

# Install our python runtime
RUN pyenv update \
    && pyenv install $PYTHON_RUNTIME_VERSION \
    && pyenv global $PYTHON_RUNTIME_VERSION \
    && pip install --upgrade pip


# APPLICATION DEPENDENCIES
# ========================

WORKDIR $PROJECT_ROOT

COPY requirements*.txt ./
RUN pip install -r requirements-local.txt


# ENTRYPOINTS AND STARTUP SCRIPTS
# ===============================

COPY ./compose/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

ENTRYPOINT ["/entrypoint"]
