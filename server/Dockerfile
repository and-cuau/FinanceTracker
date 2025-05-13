# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.9
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/app" \
    --shell "/sbin/nologin" \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Copy the source code into the container.
COPY . .

# Copy the database file explicitly
COPY transactions.db /app/

# Ensure appuser has access to /app directory and transactions.db
RUN chown -R appuser:appuser /app && chmod 664 /app/transactions.db

# Switch to the non-privileged user
USER appuser

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["python", "fintrack.py"]