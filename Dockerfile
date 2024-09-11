FROM python:3.9-alpine3.13
LABEL maintainer="Clement Hamon"

# tell python to run in unbuffered mode
# this is recommended when running python in docker containers
# because it doesn't allow python to buffer the outputs
# it just prints them directly
# this avoids some complications and makes it easier to debug
# python applications running in docker containers
ENV PYTHONUNBUFFERED=1
# Copy the requirements.txt file to the /tmp directory inside the container
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Copy the entire app directory to the /app directory inside the container
COPY ./app /app

# Set the working directory to /app
WORKDIR /app

# Expose port 8000 to allow incoming connections
EXPOSE 8000

ARG DEV=false
# Update the package index and install necessary dependencies for building Python packages
# Create a Python virtual environment at /py
RUN python -m venv /py && \
    # Upgrade pip inside the virtual environment
    /py/bin/pip install --upgrade pip && \
    # Install the required packages from the requirements.txt file
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    # Remove the temporary requirements.txt file
    rm -rf /tmp && \
    # Create a non-root user named "django-user" without a home directory
    adduser \
        --disabled-password \
        --no-create-home \
        django-user
RUN pip install --no-cache-dir flake8
ENV PATH="/py/bin:$PATH"

USER django-user

