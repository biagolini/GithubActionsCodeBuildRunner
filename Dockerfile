# The base image comes from Amazon ECR Public. The tag is multi-architecture, so the
# image that is pulled matches the CPU of the runner and nothing is emulated.
FROM public.ecr.aws/docker/library/python:3.13-slim

WORKDIR /app
RUN useradd --system --uid 10001 --no-create-home app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

USER app
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "src.app:app"]
