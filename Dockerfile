FROM    python:3.9
ARG     POETRY_VERSION=1.1.12

ENV     PYTHONUNBUFFERED=1 PYTHONPYCACHEPREFIX=/var/lib/pycache PATH=/root/.poetry/bin:$PATH
RUN     mkdir /var/lib/pycache

ADD     https://raw.githubusercontent.com/python-poetry/poetry/${POETRY_VERSION}/get-poetry.py /get-poetry.py
RUN     python /get-poetry.py --version ${POETRY_VERSION} --yes --no-modify-path && \
        poetry config virtualenvs.create false

WORKDIR /
COPY    pyproject.toml poetry.lock /remotodojo/
WORKDIR /remotodojo/
RUN     poetry install --no-interaction --no-ansi -E prod --no-dev --no-root

#       Install again after copying whole source, so that `remotodojo` and `apps` are installed.
COPY    . /remotodojo/
RUN     poetry install --no-interaction --no-ansi -E prod --no-dev

CMD     ["./server/server.sh"]
