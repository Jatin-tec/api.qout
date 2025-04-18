# E-commerce Store Project

## Project Overview

This project is a backend implementation of an e-commerce store using Django and Django REST Framework. It provides APIs for managing products, stores, user carts and user accounts. The application supports basic e-commerce functionalities such as product listing, cart management and user authentication.

## Features

- **Product Management:** Allows creation, retrieval, and management of products, including details like name, description, price, and stock.
- **Store Management:** Supports multiple stores, each with its own inventory of products.
- **User Carts:** Enables users to add products to their carts and manage quantities.
- **User Authentication:** Provides user registration and login functionalities.
- **API Endpoints:** Well-defined RESTful APIs for interacting with the application.

## Technologies Used

- **Django:** A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **Django REST Framework:** A powerful and flexible toolkit for building Web APIs.
- **PostgreSQL:** A robust open-source relational database system.
- **Docker:** A platform to develop, ship, and run applications inside containers.
- **Nginx:** A web server that can also be used as a reverse proxy, load balancer and HTTP cache.

## Setup Instructions

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Steps

1. **Clone the repository:**
```
bash
   git clone <repository-url>
   cd <project-directory>
   
```
2. **Build and run the Docker containers:**
```
bash
   docker-compose up --build
   
```
3. **Apply database migrations:**
```
bash
   docker-compose exec web python manage.py migrate
   
```
4. **Create a superuser (optional):**
```
bash
   docker-compose exec web python manage.py createsuperuser
   
```
5. **Access the application:**
   The API should now be accessible at `http://localhost:8000/`.

## API Endpoints

### User Endpoints

- **Register a new user:**
  - **Endpoint:** `/users/register/`
  - **Method:** `POST`
  - **Request Body:**
    

## Project Structure

- `carts/`: Contains the implementation for managing user carts.
- `products/`: Handles product and category management.
- `store/`: Manages store information and their association with products.
- `users/`: Implements user authentication and profiles.
- `project/`: Django project settings and URL configurations.
- `nginx/`: Nginx configuration for serving the application.
- `docker-compose.yml`: Docker Compose file for defining and running multi-container Docker applications.
- `Dockerfile`: Dockerfile for building the Django application container.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Implement your changes.
4. Write tests to ensure the changes work as expected.
5. Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.