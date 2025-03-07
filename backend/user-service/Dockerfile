FROM python:3.11.6

RUN apt-get update && apt-get install -y redis-tools

WORKDIR /backend

COPY requirements.txt /backend/requirements.txt
COPY conftest.py /backend/conftest.py

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

COPY app /backend/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]