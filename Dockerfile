FROM python:3.7

RUN useradd --uid 1000 --create-home app
RUN pip install -U pip setuptools ipython

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

COPY . /opt/project
RUN chown -R app:app /opt/project

WORKDIR /opt/project
USER app

ENV PYTHONPATH=.
ENV HOME=/home/app

VOLUME ["/home/app"]

ENTRYPOINT ["/opt/project/entrypoint.sh"]
CMD ["uwsgi", "uwsgi.ini"]
