FROM python:3.8
RUN apt update -y && apt install awscli -y
WORKDIR /app

COPY . /app
RUN pip install -r /app/requirements.txt

#CMD ["python", "main.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]