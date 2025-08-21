# ☕ Coffee Shop

A simple web application for managing and ordering coffee products.  
The backend is built with **Django** and **Django REST Framework**, while the frontend is developed with **HTML & CSS**.  
The project also includes **Docker** and **Docker Compose** support for easy setup and deployment.

## 🚀 Features
- Browse coffee products and place orders  
- RESTful API powered by Django REST Framework  
- Simple and responsive frontend with HTML & CSS  
- Ready-to-use Docker and Docker Compose configuration  

## 🛠 Tech Stack
- **Backend:** Django, Django REST Framework  
- **Frontend:** HTML, CSS  
- **Database:** SQLite (default)  
- **Deployment:** Docker, Docker Compose  

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
- For testing the API, you can use the Postman collection included in this repository:
- Import the file into Postman.
- Run the Django server.
- Execute the requests directly in Postman.
