FROM python:3.8
RUN apt update -y && apt install awscli -y
WORKDIR /app

COPY . /app
RUN pip3 install -r requirements.txt

EXPOSE 80
CMD ["python3", "main.py"]