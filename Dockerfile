FROM public.ecr.aws/bitnami/python:3.9-prod

WORKDIR /code/app

COPY . /code/app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--log-level", "critical", "--no-access-log"]

EXPOSE 80
