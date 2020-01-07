FROM python:3.5-alpine
WORKDIR /code
RUN apk add --no-cache gcc libressl-dev musl-dev linux-headers libffi-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY config .
COPY lib .
COPY run.py .
COPY CreateDatabase.py .
CMD ["python", "./run.py"]