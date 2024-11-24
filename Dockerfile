FROM python:3.12.0-alpine

# this repo uses git for library management
# so we need to install git
RUN apk add --update -y git

WORKDIR /app

COPY . .

RUN pip install .

CMD ["python", "main.py"]