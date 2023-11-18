FROM pypy:latest

WORKDIR app/
COPY --link util.py util.py
COPY --link tg_bot/ tg_bot/
COPY --link db/ db/

RUN pip install -r tg_bot/requirements_pypy.txt && rm -rf /root/.cache /tmp/pip-* /tmp/pip3-packages

