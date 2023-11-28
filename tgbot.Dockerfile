# syntax=docker/dockerfile:1
FROM pypy:latest

WORKDIR app/
COPY --link tg_bot/ tg_bot/
RUN pip install -r tg_bot/requirements_pypy.txt && rm -rf /root/.cache /tmp/pip-* /tmp/pip3-packages
COPY --link util.py util.py
COPY --link config.py config.py
COPY --link db/ db/

ENV PYTHONPATH="/app"
ENTRYPOINT ["pypy3", "tg_bot/bot.py"]
# ENTRYPOINT ["/bin/bash"]
