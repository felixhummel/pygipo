FROM python:3.7

RUN useradd --uid 1000 --create-home app
RUN pip install -U pip setuptools

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

COPY . /opt/project
RUN chown -R app:app /opt/project

WORKDIR /opt/project
USER app

VOLUME ["/home/app"]

ENTRYPOINT ["/opt/project/entrypoint.sh"]
CMD ["uwsgi", "uwsgi.ini"]
