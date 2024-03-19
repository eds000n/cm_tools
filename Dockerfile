# Use the official Python image from Docker Hub
FROM python:3.11-alpine3.18

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG OPENAI_API_KEY

ENV OPENAI_API_KEY=${OPENAI_API_KEY:-v1.0.0}

RUN apk update && apk upgrade && apk add --no-cache ffmpeg

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Copy .env file into the container
COPY .env .

CMD "echo $OPENAI_API_KEY"

# Run the FastAPI application
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
