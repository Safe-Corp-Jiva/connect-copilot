FROM public.ecr.aws/lambda/python:3.10

ENV DEV true

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --no-cache-dir -r requirements.txt

COPY . ${LAMBDA_TASK_ROOT}

CMD ["entry.handler"]