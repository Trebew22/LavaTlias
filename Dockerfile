FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWEITEBYTECODE=1

RUN useradd -ms /bin/bash python
RUN pip install --upgrade pip pipenv
COPY Pipfile* ./
RUN pipenv install --system

USER python
WORKDIR /home/tlias
COPY . .
CMD ["tail", "-f", "/dev/null"]