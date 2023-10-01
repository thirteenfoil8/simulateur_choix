FROM python:3.10

COPY ./src ./src
COPY setup.py .
COPY .env .
ENV DOTENV_PATH=/.env
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN pip install -e .

EXPOSE 5000

WORKDIR ./src/simulateur_choix/app

CMD ["python", "app.py"]
