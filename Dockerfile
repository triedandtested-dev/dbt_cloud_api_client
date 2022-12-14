FROM python:3.7
WORKDIR /app
COPY . /app
RUN pip3 install -r dev-requirements.txt
