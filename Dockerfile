# Use an official Python runtime as a parent image (Debian-based)
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary dependencies for building and audio libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    pulseaudio \
    pavucontrol \
    alsa-utils \
    ffmpeg \
    sudo \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user and switch to it
RUN useradd -ms /bin/bash vscode
USER vscode

# Copy the current directory contents into the container at /app
COPY --chown=vscode:vscode . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose necessary ports
EXPOSE 8000
EXPOSE 4713

# Define environment variable
ENV PYTHONUNBUFFERED=1
