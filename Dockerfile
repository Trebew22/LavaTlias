FROM python:3.10-slim
RUN useradd -ms /bin/bash python
RUN pip install pipenv
RUN pipenv install
USER python
WORKDIR /home/python/app
ENV PIPENV_VENV_IN_PROJECT=True
CMD ["tail", "-f", "/dev/null"]