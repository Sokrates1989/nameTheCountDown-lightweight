# Linux os for docker containers.
FROM alpine

## PYTHON.
# Install python
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python

# Activate python venv.
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN $VIRTUAL_ENV/bin/python3 -m pip install --upgrade pip

# Install pip.
RUN $VIRTUAL_ENV/bin/python3 -m ensurepip

# Install pip dependencies.
RUN pip install telepot
RUN pip install pyTelegramBotApi
RUN pip install mysql-connector-python

# Updgrade pip dependencies.
RUN pip install telepot --upgrade 


## Wait until "db" container is responsive.
# We need bash for this to work.
RUN apk update && apk add bash

# Make wait script executable.
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod 755 /wait-for-it.sh

# Copy the app.
WORKDIR /code
COPY . /code