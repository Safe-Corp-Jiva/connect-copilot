FROM public.ecr.aws/docker/library/python:3.10-slim-bullseye
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.1 /lambda-adapter /opt/extensions/lambda-adapter

ENV DEV true

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir fastapi uvicorn

COPY . .

CMD ["python", "server.py"]