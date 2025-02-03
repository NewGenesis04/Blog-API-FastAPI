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

# Introduction

This project is a FastAPI-based application designed to manage blogs, users, comments, and follow relationships. It includes features such as user authentication, role-based authorization, CRUD operations for blogs and comments, and the ability to follow/unfollow other users.

# Authentication and Authorization

The application uses JWT-based authentication with role-based access control. Users can have one of the following roles:

- **reader** : Can read blogs and create comments.
- **author** : Can create, update, and delete their own blogs and comments.
- **admin** : Has full control over all resources.

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
- **Request**: No request body required.


    