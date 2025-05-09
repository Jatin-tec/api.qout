FROM python:3.11.4-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update
RUN apt install python3-pip python3-dev libpq-dev postgresql-contrib -y

# Install tzdata
RUN apt-get update && apt-get install -y tzdata

# Set the timezone
ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Set work directory
WORKDIR /usr/src/app

# Copy the rest of the project into the container
COPY . .

# Ensure entrypoint.sh is executable
# RUN ["chmod", "+x", "./entrypoint.sh"]

# Run entrypoint.sh
# ENTRYPOINT ["./entrypoint.sh"]