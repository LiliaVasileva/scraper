# Screper

The Web Screenshot Service is a Django-based web application designed to capture screenshots of web pages starting from
a specified URL and following a specified number of links.
It leverages Celery for asynchronous task processing, allowing users to initiate screenshot tasks that run independently
in the background.

## Setting Up

This guide provides instructions for setting up a Django web application integrated with Swagger for API documentation
and Celery and Redis for task management.

It covers the installation process, project structure, and how to implement and document the provided endpoints.

## Prerequisites

- Python installed on your system
- Basic understanding of Django, Django REST Framework, Celery and Redis

## Installation

**1.Clone the Repository:**

   ```bash
   git clone https://github.com/LiliaVasileva/scraper.git
   cd scraper/
   ```

**2.Create a Virtual Environment:**

   ```bash
   python3 -m venv venv
   ```

**3.Activate the Virtual Environment:**

On Windows:

   ```bash
   venv\Scripts\activate
 ```

On macOS and Linux:

   ```bash
   source venv/bin/activate
 ```

**4.Install Dependencies:**

   ```bash
   pip install -r requirements.txt 
   ```

**5.Database set up and model creation:**

To set up the database and create models for scraper, follow these steps:

5.1. Navigate to django project directory in the terminal.

5.2. Run the following commands:

   ```bash
   cd scraper/
   python manage.py makemigrations
   python manage.py migrate
   ```

**6.Run a Celery worker to start processing tasks:. :**

Ensure that Redis is running.
Open new terminal. Make sure in you are inside the root project dir.Activate the venv and run.

   ```bash
   
    celery -A scraper.screenshots.celery worker -l INFO

   ```

**7. Run the application to navigate through the endpoints. :**

Open new terminal. Make sure in you are inside the root project dir.Activate the venv and run.
Run the following command to run the Django development server:

   ```bash
   
   python manage.py runserver
   
   ```

Once the server is running, you can access the application and its endpoints
by opening a web browser and navigating to the URL provided by the Django development server - http://127.0.0.1:8000/
When you navigate to http://127.0.0.1:8000/ in your web browser, you will be presented with the Swagger documentation
interface,
allowing you to interactively explore the API endpoints of scraper application. You can
explore and by manually typing the implemented endpoints bellow in your web browser.

**8.Implemented Endpoints:**

| Endpoints             | HTTP Method | Description                                               |
|-----------------------|-------------|-----------------------------------------------------------|
| /api/screenshots/     | POST        | Start a new screenshot task with start_url and num_links. |
| /api/screenshots/{id} | GET         | Retrieve screenshots data for a specific task ID.         |
| /api/isalive/         | GET         | API verify if the server is running.                      |

### Start a new screenshot task

**Endpoint**: `/api/screenshots/ `  
**Method**: `POST`  
**Description**: Start a new screenshot task with start_url and num_links.

**Form data**: `start_url` (required)  , `num_links` (required).

**Example**:

   ```bash
{
    "task_id": "67e179c5-f60f-4c7a-8694-771592f94b37"
}
   ```

### Retrieve screenshots data for a specific task ID.

**Endpoint**: `/api/screenshots/{id}`  
**Method**: `GET`  
**Description**: API which returns screenshots data for a specific task ID.  


**Example**:

   ```bash
{
        "id": 1,
        "task": 1,
        "url": "https://someur/",
        "image": "/image.png",
        "created_at": "2024-07-08T08:03:46.816126Z"
    }
   ```

### API verify if the server is running

**Endpoint**: `/api/isalive/`  
**Method**: `POST`  
**Description**: API verify if the server is running.  

**Example**:

   ```bash
{
    "status": "alive"
}
   ```



