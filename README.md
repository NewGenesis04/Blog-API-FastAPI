# Table of Contents

- [Introduction](#introduction)
- [Authentication and Authorization](#authentication-and-authorization)
- [User Management](#user-management)
- [Blog Management](#blog-management)
- [Follow Management](#follow-management)
- [Comment Management](#comment-management)
- [Pydantic Schemas](#pydantic-schemas)
- [Dependencies and Libraries](#dependencies-and-libraries)
- [Installation and Setup](#installation-and-setup)
- [Contributing](#contributing)
- [License](#license)

# Introduction

This project is a FastAPI-based blog management system that provides a robust and scalable backend for handling blogs, users, comments, and follow relationships. Built with performance and security in mind, it offers a seamless experience for user authentication, role-based access control, and efficient content management.

### Key Features:
- ✅ User Authentication & Authorization – Secure login, JWT-based authentication, and role-based access control (admin, author, reader).
- ✅ Blog Management – Create, update, delete, and retrieve blogs with structured data handling.
- ✅ User & Follow System – Allow users to follow/unfollow others and manage their social interactions.
- ✅ Comment System – Enable users to add, edit, and delete comments on blog posts.
- ✅ Fast & Scalable – Powered by FastAPI, ensuring high performance with asynchronous request handling.
- ✅ Database Integration – Uses MySQL with SQLAlchemy for efficient data management.
- ✅ Environment Configuration – Secure .env file usage for managing sensitive configurations.

This API serves as a foundation for blog-based applications and can be extended to support additional features like notifications, analytics, and more. 🚀

# Authentication and Authorization

The application uses JWT-based authentication with role-based access control. Users can have one of the following roles:

- **reader** : Can read blogs and create comments.
- **author** : Can create, update, and delete their own blogs and comments.
- **admin** : Has full control over all resources.

### 1. Login

- **Endpoint**: /auth/login
- **Method**: POST
- **Request**:

    ```json
    {
        "username": "author1",
        "password": "password123"
    }
    ```
- **Response(Success)**:

    ```json
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer"
    }
    ```

### 2. Register

- **Endpoint**: /auth/register
- **Method**: POST
- **Request**:

    ```json
    {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123",
        "role": "author"
    }
    ```
- **Response(Success)**:

    ```json
    {
        "id": 3,
        "username": "newuser",
        "email": "newuser@example.com",
        "role": "author"
    }
    ```

Endpoints requiring authentication are protected using **get_current_user**, while specific roles are enforced using **role_required**

# User Management

## Routes
### 1. Get All Users
- **Endpoint**: /user/all
- **Method**: GET
- **Description**: Fetches all users (requires admin or author role).
- **Request**: No request body required.
- **Response(Success)**:

    ```json
    [
        {
            "id": 1,
            "username": "author1",
            "email": "author1@example.com",
            "role": "author"
        },
        {
            "id": 2,
            "username": "reader1",
            "email": "reader1@example.com",
            "role": "reader"
        }
    ]
    
### 2. Get Current User
- **Endpoint**: /user/current
- **Method**: GET
- **Description**: Fetches the currently authenticated user.
- **Request**: No request body required.
- **Response(Success)**:

    ```json
    {
    "id": 1,
    "username": "author1",
    "email": "author1@example.com",
    "role": "author"
    }

### 3. Update User
- **Endpoint**: /user/update
- **Method**: PUT
- **Description**: Updates the profile of the currently authenticated user.
- **Request**:

    ``` json
    {
    "username": "updatedAuthor",
    "email": "updated.author@example.com",
    "bio": "This is my updated bio."
    }
- **Response(Success)**:
    ```json
    {
    "detail": "User with id(1) has been updated"
    }

### 4. Delete User
- **Endpoint**: /user/delete
- **Method**: DELETE
- **Description**: Deletes the currently authenticated user.
- **Request**: No request body required.
- **Response(Success)**: 

    ``` json
    {
    "detail": "User with name: author1 and id: 1 has been deleted"
    }

# Blog Management

## Routes

### 1. Create Blog
- Endpoint : /blog/
- Method : POST
- Description : Creates a new blog post. Admins can optionally specify an author ID.
- **Request**:

    ```json
    {
    "title": "New Blog Post",
    "content": "This is the content of the new blog post.",
    "published": true
    }

- **Response(Success)**: 

    ```json
    {
    "id": 1,
    "title": "New Blog Post",
    "content": "This is the content of the new blog post.",
    "author_id": 1,
    "created_at": "2023-09-25T12:00:00Z"
    }

### 2. Get All Blogs:
- **Endpoint**: /blog/
- **Method**: GET
- **Description**: Fetches all blogs or filters by a specific user ID.
- **Request**: Optional query parameter **user_id**
- **Response(Success)**:

    ``` json
    [
    {
        "id": 1,
        "title": "Blog Post 1",
        "content": "Content of Blog Post 1",
        "author_id": 1
    },
    {
        "id": 2,
        "title": "Blog Post 2",
        "content": "Content of Blog Post 2",
        "author_id": 2
    }
    ]

### 3. Get Current User's Blogs
- **Endpoint**: /blog/current
- **Method**: GET
- **Description**: Fetches all blogs authored by the currently authenticated user.
- **Request**: No request body required.
- **Response(Success)**:

    ```json
    [
    {
        "id": 1,
        "title": "Blog Post 1",
        "content": "Content of Blog Post 1",
        "author_id": 1
    }
    ]

### 4. Get Blog by ID
- **Endpoint**: /blog/{id}
- **Method**: GET
- **Description**: Fetches a specific blog by its ID.
- **Request**: No request body required.
- **Response(Success)**: 

    ``` json
    {
    "id": 1,
    "title": "Blog Post 1",
    "content": "Content of Blog Post 1",
    "author_id": 1,
    "created_at": "2023-09-25T12:00:00Z"
    }

5. Update Blog
- **Endpoint**: /blog/{id}
- **Method**: PUT
- **Description**: Updates a specific blog post. Only the author of the blog can perform this action.
- **Request**:

    ``` json
    {
    "title": "Updated Blog Title",
    "content": "Updated content of the blog post.",
    "published": false
    }

- **Response(Success)**:

    ``` json
    {
    "title": "Updated Blog Title",
    "content": "Updated content of the blog post.",
    "published": false
    }

### 6. Delete Blog
- **Endpoint**: /blog/{id}
- **Method**: DELETE
- **Description**: Deletes a specific blog post. Only the author or an admin can perform this action.
- **Request**:
No request body required.
- **Response(Success)**:

    ``` json
    {
    "detail": "Blog with id(1) deleted"
    }

# Follow Management

### 1. Follow User
- **Endpoint**: /follow/{userId}
- **Method**: POST
- **Description**: Allows the authenticated user to follow another user by their ID.
- **Request**:No request body required.
- **Response(Success)**:

    ```json
    {
    "detail": "User with id(2) has been followed"
    }

### 2. Unfollow User
- **Endpoint**: /follow/{userId}
- **Method**: DELETE
- **Description**: Allows the authenticated user to unfollow another user by their ID.
- **Request**: No request body required.
- **Response(Success)**:

    ``` json
    {
    "detail": "User with id(2) has been unfollowed"
    }

### 3. Get Following List
- **Endpoint**: /follow/following
- **Method**: GET
- **Description**: Retrieves the list of users that the authenticated user is following. Optionally, it can retrieve the following list for another user by specifying their ID.
- **Request**: Optional query parameter **alt_user**.
- **Response(Success)**:

    ``` json
    [
    {
        "id": 2,
        "username": "user2",
        "email": "user2@example.com",
        "role": "author"
    },
    {
        "id": 3,
        "username": "user3",
        "email": "user3@example.com",
        "role": "reader"
    }
    ]

### 4. Get Followers List
- **Endpoint**: /follow/followers
- **Method**: GET
- **Description**: Retrieves the list of users who are following the authenticated user. Optionally, it can retrieve the followers list for another user by specifying their ID.
- **Request**:Optional query parameter **alt_user**.
- **Response(Success)**:

    ``` json
    [
    {
        "id": 1,
        "username": "author1",
        "email": "author1@example.com",
        "role": "author"
    },
    {
        "id": 4,
        "username": "reader2",
        "email": "reader2@example.com",
        "role": "reader"
    }
    ]

# Comment Management

### 1. Create Comment
- **Endpoint**: /comment/{blogId}
- **Method**: POST
- **Description**: Allows the authenticated user to create a new comment on a specific blog post.
- **Request**: 

    ``` json
    {
    "content": "This is a great blog post!"
    }

- **Response(Success)**:

    ``` json
    {
    "id": 1,
    "author_id": 1,
    "blog_id": 1,
    "content": "This is a great blog post!",
    "created_at": "2023-09-25T12:00:00Z"
    }

### 2. Get Comments
- **Endpoint**: /comment/{blogId}
- **Method**: GET
- **Description**: Retrieves comments for a specific blog post. Supports filtering by author ID or fetching all comments (if authorized).
- **Request**: Optional query parameters **author_id** or **include_all**.
- **Response(Success)**:

    ``` json
    [
    {
        "id": 1,
        "author_id": 1,
        "blog_id": 1,
        "content": "This is a great blog post!",
        "created_at": "2023-09-25T12:00:00Z"
    },
    {
        "id": 2,
        "author_id": 2,
        "blog_id": 1,
        "content": "I agree with you.",
        "created_at": "2023-09-25T13:00:00Z"
    }
    ]

### 3. Update Comment
- **Endpoint**: /comment/{commentId}
- **Method**: PUT
- **Description**: Allows the authenticated user to update their own comment.
- **Request**:

    ``` json
    {
    "content": "Updated comment content."
    }

- **Response(Success)**:

    ``` json
    {
    "detail": "Comment with id(1) has been updated"
    }

### 4. Delete Comment
- **Endpoint**: /comment/{commentId}
- **Method**: DELETE
- **Description**: Allows the authenticated user to delete their own comment.
- **Request**: No request body required.
- **Response(Success)**:

    ```json
    {
    "detail": "Comment with id(1) has been deleted"
    }

# Dependencies and Libraries

This application relies on the following key libraries:

- FastAPI: High-performance web framework for building APIs.
- SQLAlchemy: ORM for database interactions.
- Alembic: Database migration tool.
- Pydantic: Data validation and settings management.
- Passlib: Password hashing library.
- JWT: JSON Web Token implementation for authentication.
- Uvicorn: ASGI server for running the application.
- Starlette: Underlying framework for FastAPI.

# Installation and Setup

## Prerequisites

Before installing the dependencies, ensure that the following are installed on your system:

### 1. Python 3.10+:
The application requires Python version 3.10 or higher. You can verify your Python version by running:

```sh
python --version
```

If Python is not installed, download it from [python.org](https://www.python.org/).

### 2. Pip: 
Ensure that pip (Python's package installer) is installed. You can check this by running:

```sh
pip --version
```

## Steps

### 1. Clone the Repository:

```sh
git clone https://github.com/NewGenesis04/Blog-API-FastAPI.git
cd Blog-Fast-API
```

### 2. Set Up Virtual Environment:

```sh
python -m venv .venv
.venv\Scripts\activate 
```

### 3. Install Dependencies:

```sh
pip install -r requirements.txt
```

### 4. Configure Environment Variables:
Create a .env file in the root directory and configure the following:

```ini
DATABASE_URL="mysql+pymysql://username:password@localhost/db_name"
JWT_SECRET_KEY="your-secret-key"
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60
```
    
### 5. Run Migrations:

Delete the alembic folder and run these commands:

```sh
alembic init
```

Modify the alembic/env.py file:
```sh
from dotenv import load_dotenv
import os
load_dotenv()
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))
```
Create migration file:

```sh
alembic revision -m "Your migration message"
```

Apply migrations to the database:

```sh
alembic upgrade head
```

### 6. Start the Application:

```sh
uvicorn app.main:app --reload
```

# Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

# License
This project is licensed under the MIT License. See the **LICENSE** file for details.