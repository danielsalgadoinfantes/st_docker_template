FROM python:3.10.9

COPY requirements.txt app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8802 

CMD ["streamlit", "run", "app.py"]
