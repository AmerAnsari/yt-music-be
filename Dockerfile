FROM python:slim-buster

ENV PYTHONUNBUFFERED 1

# Install dependencies and clean up in a single RUN step
RUN apt-get update \
  # Install necessary dependencies for building Python packages
  && apt-get install -y \
    build-essential \
    gettext \
    libmagic-dev \
    libpq-dev \
  # Clean up unused files and caches to reduce image size
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Set up application directories
RUN mkdir /code
WORKDIR /code

# Copy requirements and install them first to leverage Docker layer caching
COPY ./requirements*.txt ./
RUN pip --no-cache-dir install --prefer-binary -r requirements.txt

# Copy the rest of the application code
COPY . .

RUN npm install

# Ensure docker_entry_point.sh is executable
RUN chmod +x /code/bin/docker_entry_point.sh

EXPOSE 8000

ENTRYPOINT ["sh", "-c", "/code/bin/docker_entry_point.sh"]
