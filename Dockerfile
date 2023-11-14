FROM python:3.11

WORKDIR /api

COPY ./skills_guide_api /api/skills_guide_api
COPY ./app.py /api
COPY ./config.py /api
COPY ./requirements.txt /api
COPY ./README.md /api

RUN python -m pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
