# Use the official Node.js image as the base image
FROM node:lts-slim AS node-build

# Set up application directories for Node.js
WORKDIR /code

# Copy package.json and package-lock.json for npm dependencies
COPY package*.json ./

# Install node modules
RUN npm install

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

# Copy the installed node_modules from the node-build stage
COPY --from=node-build /code/node_modules ./node_modules
COPY --from=node-build /code/package*.json ./

# Copy the rest of the application code
COPY . .

# Ensure docker_entry_point.sh is executable
RUN chmod +x /code/bin/docker_entry_point.sh

EXPOSE 8000

ENTRYPOINT ["sh", "-c", "/code/bin/docker_entry_point.sh"]
