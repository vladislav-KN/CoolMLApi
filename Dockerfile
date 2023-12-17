FROM python:3.10
LABEL authors="NCat"

ENV ENV=${ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONPATH=/code/ \
  # Disable pip cache to make docker image smaller
  PIP_NO_CACHE_DIR=1 \
  # Disable pip version check
  PIP_DISABLE_PIP_VERSION_CHECK=1



COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install python-multipart
RUN pip install requests
COPY ./app /code/app
WORKDIR /code/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]