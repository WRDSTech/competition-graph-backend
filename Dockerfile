FROM python:3.10-slim-buster

WORKDIR /backend

COPY requirements.txt /backend
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /backend

EXPOSE 8000
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--timeout", "120", "app.factory:create_app()"]

# uvicorn --reload