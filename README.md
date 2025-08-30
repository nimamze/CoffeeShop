# ☕ Coffee Shop

A simple web application for managing and ordering coffee products.  
The backend is built with **Django** and **Django REST Framework**, while the frontend is developed with **HTML & CSS**.  
The project also includes **Docker** and **Docker Compose** support for easy setup and deployment.  

## 🚀 Features
- Browse coffee products and place orders  
- User authentication with **JWT (access & refresh tokens)**  
- RESTful API powered by Django REST Framework  
- **Swagger (drf-yasg)** API documentation  
- File storage using **Boto3 with Arvan Cloud (S3 compatible)**  
- Static & media file management  
- Simple and responsive frontend with HTML & CSS  
- Ready-to-use Docker and Docker Compose configuration  

## 🛠 Tech Stack
- **Backend:** Django, Django REST Framework  
- **Frontend:** HTML, CSS  
- **Database:** SQLite (default)  
- **Authentication:** JWT Authentication  
- **API Documentation:** Swagger (drf-yasg)  
- **Deployment:** Docker, Docker Compose  
- **Storage:** Boto3, Arvan Cloud Object Storage, Static Files Management  

## 📦 Installation

### Run locally
```bash
git clone https://github.com/your-username/coffee-shop.git
cd coffee-shop

python -m venv venv
source venv/bin/activate   # Linux & Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
## 📮 Postman Collection

For testing the API, you can use the Postman collection included in this repository.  
It contains endpoints for authentication, product management, and orders.  
Simply import the file into Postman, run the Django server, and execute the requests directly.
