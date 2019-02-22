FROM python:3.6
ENV PYTHONUNBUFFERED 1

# Set apps home directory.
ENV APP_DIR /code
RUN mkdir ${APP_DIR}

# Define current working directory.
WORKDIR ${APP_DIR}

# Python module install
ADD requirements.txt ${APP_DIR}/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . ${APP_DIR}/

# Cleanup
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
