FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends
RUN pip install --upgrade pip
RUN pip install dbt-mysql

# Set the working directorydocker build -t my-dbt-image .

WORKDIR /app

# Copy your dbt project files into the container
COPY . /app

# Set environment variables for dbt
ENV DBT_PROFILE_DIR=/app
ENV DBT_PROJECT_DIR=/app

# Set default command for the container
CMD ["tail", "-f", "/dev/null"]