# pull official base image
FROM python:3.9.9-slim-buster

# set working directory
WORKDIR /usr/src/app/

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

# exposes the port 8000 to outside wold.
EXPOSE 8000

# run app
ENTRYPOINT [ "uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]

