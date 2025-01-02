FROM python:3.11.8-slim

# Set a working directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Poetry
RUN pip install --upgrade pip \
    && pip install poetry

# Copy only the necessary files for installing dependencies
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the application files
COPY . .

# Command to run the application can be added here, for example:
# CMD ["python", "app.py"]
