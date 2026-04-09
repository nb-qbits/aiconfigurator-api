FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git git-lfs && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN git clone https://github.com/ai-dynamo/aiconfigurator.git && \
    cd aiconfigurator && \
    git lfs install && \
    git lfs pull && \
    cd .. && \
    pip install --no-cache-dir -e ./aiconfigurator

EXPOSE 10000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
