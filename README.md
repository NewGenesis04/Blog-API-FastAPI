# Blog App API

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/NewGenesis04/Blog-API-FastAPI)

## Overview
This project is a high-performance FastAPI-based blog management system, providing a robust and scalable backend for handling user authentication, content management for blogs and comments, user following, and file uploads. It is built using Python, FastAPI, SQLAlchemy for ORM, and integrates with Cloudinary for media storage, backed by a relational database (MySQL/PostgreSQL compatible).

For an in-depth documentation powered by AI checkout: [DeepWiki](https://deepwiki.com/NewGenesis04/Blog-API-FastAPI)

## Features
- **User Authentication**: JWT-based authentication for secure access, including registration, login, token refresh, and password management.
- **Role-Based Access Control (RBAC)**: Differentiated access levels for `admin`, `author`, and `reader` roles.
- **User Management**: Comprehensive CRUD operations for user profiles, including biography, job descriptions, and profile/cover photo uploads.
- **Blog Management**: Full CRUD capabilities for blog posts, supporting content publishing, tagging, and like functionality.
- **Comment System**: Users can comment on blog posts, and comments can also be liked.
- **Follow System**: Users can follow and unfollow other users, and view their followers and following lists.
- **File Uploads**: Seamless integration with Cloudinary for handling profile pictures and cover photos.
- **Database Migrations**: Alembic for managing and versioning database schema changes.
- **Structured Logging**: Configurable logging setup for better observability.
- **CORS Support**: Configured to handle cross-origin requests for frontend integration.

## Getting Started
To get this project up and running on your local machine, follow these steps.

### Installation
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/NewGenesis04/Blog-API-FastAPI.git
    cd Blog-API-FastAPI
    ```
2.  **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    ```
3.  **Activate the Virtual Environment**:
    *   **On macOS/Linux**:
        ```bash
        source venv/bin/activate
        ```
    *   **On Windows**:
        ```bash
        .\venv\Scripts\activate
        ```
4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Initialize Database and Run Migrations**:
    Ensure your database (e.g., MySQL or PostgreSQL) is running and accessible via the `DATABASE_URL` configured in your `.env` file.
    ```bash
    alembic upgrade head
    ```

### Environment Variables
Create a `.env` file in the root directory of the project based on the `.env.sample` provided, and populate it with your specific configurations.

| Variable                      | Description                                                  | Example Value                                       |
| :---------------------------- | :----------------------------------------------------------- | :-------------------------------------------------- |
| `DATABASE_URL`                | Connection string for your database.                         | `mysql+pymysql://user:password@host:port/dbname` or `postgresql+psycopg2://user:password@host:port/dbname` |
| `SECRET_KEY`                  | A strong secret key for general application security.        | `my_super_secure_app_key_123`                       |
| `JWT_SECRET_KEY`              | A strong secret key for signing JWT tokens.                  | `another_very_secret_jwt_key`                       |
| `JWT_ALGORITHM`               | Algorithm used for JWT token signing.                        | `HS256`                                             |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiration time for access tokens in minutes.                | `15`                                                |
| `CLOUDINARY_API_SECRET`       | Cloudinary API Secret for image management.                  | `your_cloudinary_api_secret`                        |
| `CLOUDINARY_API_KEY`          | Cloudinary API Key for image management.                     | `your_cloudinary_api_key`                           |
| `CLOUDINARY_CLOUD_NAME`       | Cloudinary Cloud Name for your account.                      | `your_cloudinary_cloud_name`                        |

### Running the Application
Once the dependencies are installed and environment variables are set, you can run the FastAPI application:

```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.

## Usage
The API provides a comprehensive set of endpoints for managing users, blogs, comments, and interactions.
After starting the application, you can access the interactive API documentation (Swagger UI) at `http://localhost:8000/docs` or ReDoc at `http://localhost:8000/redoc`.

**Example Usage: User Registration and Login**

1.  **Register a new user:**
    ```bash
    curl -X POST "http://localhost:8000/auth/register" \
         -H "Content-Type: application/json" \
         -d '{
               "username": "testuser",
               "email": "test@example.com",
               "password": "StrongPassword123",
               "role": "author"
             }'
    ```
    *Successful Response Example:*
    ```json
    {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com",
      "role": "author",
      "bio": null,
      "profile_url": null,
      "cover_photo_url": null,
      "created_at": "2024-01-01T12:00:00"
    }
    ```

2.  **Login to get tokens:**
    ```bash
    curl -X POST "http://localhost:8000/auth/login" \
         -H "Content-Type: application/json" \
         -d '{
               "identifier": "test@example.com",
               "password": "StrongPassword123"
             }'
    ```
    *Successful Response Example:*
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer"
    }
    ```
    Use the `access_token` in the `Authorization: Bearer <token>` header for authenticated endpoints.

## API Documentation
### Base URL
`http://localhost:8000`

### Endpoints

#### POST /auth/login
**Overview**: Authenticates a user and returns JWT tokens.
**Request**:
```json
{
  "identifier": "string",
  "password": "string"
}
```
**Response**:
```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "bearer"
}
```
**Errors**:
- 400 Bad Request: Incorrect username/email or password.

#### GET /auth/me
**Overview**: Returns the current authenticated user's profile.
**Request**: (Requires Authorization header)
No payload.
**Response**:
```json
{
  "id": 1,
  "username": "string",
  "email": "string",
  "role": "string"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.

#### POST /auth/register
**Overview**: Creates a new user account.
**Request**:
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "role": "string (default: 'reader', options: 'reader', 'author', 'admin')"
}
```
**Response**:
```json
{
  "id": 1,
  "username": "string",
  "email": "string",
  "role": "string",
  "bio": null,
  "profile_url": null,
  "cover_photo_url": null,
  "created_at": "2024-01-01T12:00:00"
}
```
**Errors**:
- 400 Bad Request: Email already registered.
- 500 Internal Server Error: Error creating new user.

#### PUT /auth/update_password
**Overview**: Changes user password.
**Request**:
```json
{
  "old_password": "string",
  "new_password": "string"
}
```
**Response**:
```json
{
  "detail": "Password updated"
}
```
**Errors**:
- 400 Bad Request: Old password incorrect.
- 401 Unauthorized: Invalid or missing token.
- 500 Internal Server Error: Error updating password.

#### POST /auth/logout
**Overview**: Revokes the current refresh token.
**Request**: (Requires refresh token in Authorization header)
No payload.
**Response**:
```json
{
  "detail": "Refresh token revoked, user logged out succesfully"
}
```
**Errors**:
- 401 Unauthorized: Refresh token already expired or invalid.

#### POST /auth/refresh
**Overview**: Generates new access token using refresh token.
**Request**: (Requires refresh token in Authorization header)
No payload.
**Response**:
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```
**Errors**:
- 401 Unauthorized: Refresh token expired, revoked, or invalid.

#### POST /blog/
**Overview**: Creates a new blog post.
**Request**:
```json
{
  "title": "string",
  "content": "string",
  "published": true,
  "tag": "string (e.g., 'technology', 'lifestyle')",
  "published_at": "datetime (optional)",
  "author_id": "integer (optional, required if current user is admin and wants to assign)"
}
```
**Response**:
```json
{
  "id": 1,
  "title": "string",
  "content": "string",
  "created_at": "2024-01-01T12:00:00",
  "published_at": "2024-01-01T12:00:00",
  "published": true,
  "author_id": 1,
  "tag": "string",
  "like_count": 0,
  "comment_count": 0
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 403 Forbidden: User does not have `admin` or `author` role.
- 404 Not Found: Author with specified `author_id` not found (if admin).
- 500 Internal Server Error: Error creating blog.

#### GET /blog/
**Overview**: Lists blogs with optional filters.
**Request**: (Authorization header optional; unauthenticated users see only published blogs)
Query Parameters:
- `user_id`: integer (optional) - Filter by author ID.
**Response**:
```json
[
  {
    "id": 1,
    "title": "string",
    "content": "string",
    "created_at": "2024-01-01T12:00:00",
    "published_at": "2024-01-01T12:00:00",
    "published": true,
    "author_id": 1,
    "tag": "string",
    "like_count": 0,
    "comment_count": 0
  }
]
```
**Errors**:
- 404 Not Found: No blogs found matching criteria.
- 500 Internal Server Error: Error retrieving blogs.

#### GET /blog/current
**Overview**: Gets blogs by current authenticated user.
**Request**: (Requires Authorization header)
No payload.
**Response**:
```json
[
  {
    "id": 1,
    "title": "string",
    "content": "string",
    "created_at": "2024-01-01T12:00:00",
    "published_at": "2024-01-01T12:00:00",
    "published": true,
    "author_id": 1,
    "tag": "string",
    "like_count": 0,
    "comment_count": 0
  }
]
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 403 Forbidden: User does not have `admin` or `author` role.
- 404 Not Found: No blogs found for this user.
- 500 Internal Server Error: Error getting blog.

#### GET /blog/{id}
**Overview**: Gets single blog post by ID. Drafts are only visible to the owner or admin.
**Request**: (Authorization header optional; unauthenticated users see only published blogs)
Path Parameters:
- `id`: integer (required) - Blog ID.
**Response**:
```json
{
  "id": 1,
  "title": "string",
  "content": "string",
  "created_at": "2024-01-01T12:00:00",
  "published_at": "2024-01-01T12:00:00",
  "published": true,
  "author_id": 1,
  "tag": "string",
  "like_count": 0,
  "comment_count": 0
}
```
**Errors**:
- 404 Not Found: Blog not found.
- 403 Forbidden: You do not have access to this blog (if unpublished and not owner/admin).
- 500 Internal Server Error: Error getting blog.

#### PUT /blog/{id}
**Overview**: Updates blog post (author/admin only).
**Request**:
Path Parameters:
- `id`: integer (required) - Blog ID to update.
Payload:
```json
{
  "title": "string (optional)",
  "content": "string (optional)",
  "published": true (optional),
  "tag": "string (optional)"
}
```
**Response**:
```json
{
  "detail": "Blog with id(1) has been updated"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 403 Forbidden: You are not authorized to update this blog.
- 404 Not Found: Blog with specified ID not found.
- 500 Internal Server Error: Error updating blog.

#### DELETE /blog/{id}
**Overview**: Deletes blog post (author/admin only). Cascades to associated comments.
**Request**: (Requires Authorization header)
Path Parameters:
- `id`: integer (required) - Blog ID to delete.
**Response**:
```json
{
  "detail": "Blog with id(1) deleted"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 403 Forbidden: You are not authorized to delete this blog.
- 404 Not Found: Blog not found.
- 500 Internal Server Error: Error deleting blog.

#### GET /blog/tag/{tag}
**Overview**: Lists blogs filtered by tag.
**Request**: (Authorization header optional; unauthenticated users see only published blogs)
Path Parameters:
- `tag`: string (required) - Filter tag (e.g., 'technology').
**Response**:
```json
[
  {
    "id": 1,
    "title": "string",
    "content": "string",
    "created_at": "2024-01-01T12:00:00",
    "published_at": "2024-01-01T12:00:00",
    "published": true,
    "author_id": 1,
    "tag": "string"
  }
]
```
**Errors**:
- 404 Not Found: No blogs found with this tag.
- 500 Internal Server Error: Error getting blog.

#### POST /blog/like/{blog_id}
**Overview**: Likes a blog post (one like per user).
**Request**: (Requires Authorization header)
Path Parameters:
- `blog_id`: integer (required) - Target blog ID.
**Response**:
```json
{
  "detail": "Blog with id(1) has been liked"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 404 Not Found: Blog not found.
- 400 Bad Request: You have already liked this blog.

#### POST /blog/unlike/{blog_id}
**Overview**: Unlikes a blog post.
**Request**: (Requires Authorization header)
Path Parameters:
- `blog_id`: integer (required) - Target blog ID.
**Response**:
```json
{
  "detail": "Blog with id(1) has been unliked"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 404 Not Found: Blog not found.
- 400 Bad Request: You have not liked this blog.
- 500 Internal Server Error: Error unliking blog.

#### POST /comments/{blog_id}
**Overview**: Adds a comment to a blog post.
**Request**: (Requires Authorization header)
Path Parameters:
- `blog_id`: integer (required) - Target blog ID.
Payload:
```json
{
  "content": "string"
}
```
**Response**:
```json
{
  "id": 1,
  "author_id": 1,
  "blog_id": 1,
  "content": "string",
  "created_at": "2024-01-01T12:00:00"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 404 Not Found: Blog not found.
- 500 Internal Server Error: Error creating comment.

#### GET /comments/{blog_id}
**Overview**: Lists comments for a blog.
**Request**: (Authorization header optional; if not provided, may show only public comments or require specific `author_id`)
Path Parameters:
- `blog_id`: integer (required) - Target blog ID.
Query Parameters:
- `include_all`: boolean (optional) - If true, lists all comments (admin only).
- `author_id`: integer (optional) - Filter by commenter's ID.
**Response**:
```json
[
  {
    "id": 1,
    "author_id": 1,
    "blog_id": 1,
    "content": "string",
    "created_at": "2024-01-01T12:00:00",
    "likes_count": 0
  }
]
```
**Errors**:
- 404 Not Found: No comments found.
- 500 Internal Server Error: Error getting comments.

#### POST /comments/like/{comment_id}
**Overview**: Likes a comment (one like per user).
**Request**: (Requires Authorization header)
Path Parameters:
- `comment_id`: integer (required) - Target comment ID.
**Response**:
```json
{
  "detail": "Comment with id(1) has been liked"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 404 Not Found: Comment not found.
- 400 Bad Request: You have already liked this comment.
- 500 Internal Server Error: Error liking comment.

#### POST /comments/unlike/{comment_id}
**Overview**: Unlikes a comment.
**Request**: (Requires Authorization header)
Path Parameters:
- `comment_id`: integer (required) - Target comment ID.
**Response**:
```json
{
  "detail": "Comment with id(1) has been unliked"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 404 Not Found: Comment not found.
- 400 Bad Request: You have not liked this comment.
- 500 Internal Server Error: Error unliking comment.

#### PUT /comments/{comment_id}
**Overview**: Edits comment content (owner only).
**Request**: (Requires Authorization header)
Path Parameters:
- `comment_id`: integer (required) - Comment ID.
Payload:
```json
{
  "content": "string"
}
```
**Response**:
```json
{
  "id": 1,
  "author_id": 1,
  "blog_id": 1,
  "content": "string",
  "created_at": "2024-01-01T12:00:00"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 403 Forbidden: You are not authorized to update this comment.
- 404 Not Found: No comment found.
- 500 Internal Server Error: Error updating comment.

#### DELETE /comments/{comment_id}
**Overview**: Deletes comment (owner/admin).
**Request**: (Requires Authorization header)
Path Parameters:
- `comment_id`: integer (required) - Comment ID.
**Response**:
```json
{
  "detail": "Comment with id(1) has been deleted"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 403 Forbidden: You are not authorized to delete this comment.
- 404 Not Found: Comment not found.
- 500 Internal Server Error: Error deleting comment.

#### POST /files/upload-profile-pic
**Overview**: Uploads profile picture (replaces existing).
**Request**: (Requires Authorization header)
Form Data:
- `file`: file (image file, e.g., JPG, PNG, up to 5MB)
**Response**:
```json
{
  "image_url": "https://res.cloudinary.com/your_cloud_name/image/upload/v123456789/public_id.jpg"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 400 Bad Request: Error in file upload (e.g., file type, size).
- 404 Not Found: User not found.
- 500 Internal Server Error: Error uploading image.

#### GET /files/profile-pic
**Overview**: Gets the profile picture URL from the database.
**Request**: (Requires Authorization header)
No payload.
**Response**:
```json
{
  "profile_url": "https://res.cloudinary.com/your_cloud_name/image/upload/v123456789/public_id.jpg"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 404 Not Found: User does not have a profile picture.
- 500 Internal Server Error: Error retrieving profile picture.

#### GET /files/cover-photo
**Overview**: Gets the cover photo URL from the database.
**Request**: (Requires Authorization header)
No payload.
**Response**:
```json
{
  "cover_photo_url": "https://res.cloudinary.com/your_cloud_name/image/upload/v123456789/public_id.jpg"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 404 Not Found: User does not have a cover photo.
- 500 Internal Server Error: Error retrieving cover photo.

#### POST /files/upload-cover-photo
**Overview**: Uploads cover photo (replaces existing).
**Request**: (Requires Authorization header)
Form Data:
- `file`: file (image file, e.g., JPG, PNG, up to 5MB)
**Response**:
```json
{
  "image_url": "https://res.cloudinary.com/your_cloud_name/image/upload/v123456789/public_id.jpg"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 400 Bad Request: Error in file upload (e.g., file type, size).
- 500 Internal Server Error: Error uploading cover photo.

#### DELETE /files/delete-profile-pic
**Overview**: Removes user's profile picture. Deletes the image from Cloudinary.
**Request**: (Requires Authorization header)
No payload.
**Response**:
```json
{
  "detail": "Profile picture deleted"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 400 Bad Request: User does not have a profile picture.
- 404 Not Found: User not found.
- 500 Internal Server Error: Error deleting image.

#### DELETE /files/delete-cover-photo
**Overview**: Removes user's cover photo. Deletes the image from Cloudinary.
**Request**: (Requires Authorization header)
No payload.
**Response**:
```json
{
  "detail": "Profile picture deleted"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 400 Bad Request: User does not have a profile picture.
- 404 Not Found: User not found.
- 500 Internal Server Error: Error deleting image.

#### POST /follow/{userId}
**Overview**: Follows another user.
**Request**: (Requires Authorization header)
Path Parameters:
- `userId`: integer (required) - ID of user to follow.
**Response**:
```json
{
  "detail": "User with id(2) has been followed"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 404 Not Found: User not found.
- 400 Bad Request: You are already following this user.
- 500 Internal Server Error: Error following user.

#### DELETE /follow/{userId}
**Overview**: Stops following a user.
**Request**: (Requires Authorization header)
Path Parameters:
- `userId`: integer (required) - ID of user to unfollow.
**Response**:
```json
{
  "detail": "User with id(2) has been unfollowed"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 404 Not Found: User not found.
- 400 Bad Request: You are not following this user.
- 500 Internal Server Error: Error unfollowing user.

#### GET /follow/following
**Overview**: Lists users a specific user is following.
**Request**: (Requires Authorization header)
Query Parameters:
- `alt_user`: integer (optional) - Target user ID (defaults to current user).
**Response**:
```json
[
  {
    "id": 2,
    "username": "followed_user",
    "email": "followed@example.com",
    "profile_url": null,
    "created_at": "2024-01-01T12:00:00",
    "job_description": null
  }
]
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 500 Internal Server Error: Error getting following list.

#### GET /follow/followers
**Overview**: Lists followers of a specific user.
**Request**: (Requires Authorization header)
Query Parameters:
- `alt_user`: integer (optional) - Target user ID (defaults to current user).
**Response**:
```json
[
  {
    "id": 3,
    "username": "follower_user",
    "email": "follower@example.com",
    "profile_url": null,
    "created_at": "2024-01-01T12:00:00",
    "job_description": null
  }
]
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 500 Internal Server Error: Error getting followers list.

#### GET /user/all
**Overview**: Lists all users.
**Request**: (Requires Authorization header)
No payload.
**Response**:
```json
[
  {
    "id": 1,
    "username": "user1",
    "email": "user1@example.com",
    "profile_url": null,
    "created_at": "2024-01-01T12:00:00",
    "job_description": null
  }
]
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 500 Internal Server Error: Error fetching users.

#### GET /user/current
**Overview**: Returns profile of the current or specified user.
**Request**: (Requires Authorization header)
Query Parameters:
- `altId`: integer (optional) - User ID to fetch (defaults to current user).
**Response**:
```json
{
  "id": 1,
  "username": "string",
  "email": "string",
  "role": "string",
  "bio": "string",
  "profile_url": "string",
  "cover_photo_url": "string",
  "created_at": "2024-01-01T12:00:00",
  "job_description": "string"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 404 Not Found: User with specified ID not found.
- 500 Internal Server Error: Error getting user.

#### PUT /user/update
**Overview**: Updates the current authenticated user's profile.
**Request**: (Requires Authorization header)
Payload:
```json
{
  "username": "string (optional)",
  "email": "string (optional)",
  "bio": "string (optional)",
  "job_description": "string (optional)"
}
```
**Response**:
```json
{
  "detail": "User with id(1) has been updated"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 404 Not Found: User not found.
- 500 Internal Server Error: Error updating user.

#### DELETE /user/delete
**Overview**: Deletes the current authenticated user's account (irreversible).
**Request**: (Requires Authorization header)
No payload.
**Response**:
```json
{
  "detail": "User with name: username and id: 1 has been deleted"
}
```
**Errors**:
- 401 Unauthorized: Invalid or missing token.
- 404 Not Found: User not found.
- 500 Internal Server Error: Error deleting user.

## Technologies Used

| Technology    | Description                                       |
| :------------ | :------------------------------------------------ |
| Python        | Primary programming language.                     |
| FastAPI       | High-performance web framework for APIs.          |
| SQLAlchemy    | SQL toolkit and Object-Relational Mapper (ORM).   |
| Alembic       | Lightweight database migration tool.              |
| MySQL         | Relational database management system.         |
| JWT           | JSON Web Tokens for secure authentication.        |
| Cloudinary    | Cloud-based image and video management service.   |
| Uvicorn       | ASGI web server for running FastAPI applications. |
| Pydantic      | Data validation and settings management.          |

## Contributing
We welcome contributions to enhance this project! To contribute:

1.  **Fork the repository**.
2.  **Create a new branch** for your feature or bug fix: `git checkout -b feature/your-feature-name`.
3.  **Make your changes** and ensure the code adheres to existing style guidelines.
4.  **Write clear, concise commit messages**.
5.  **Submit a Pull Request** to the `main` branch, detailing your changes and their benefits.

## License
This project is licensed under the [MIT License](LICENSE).

## Author Info
**Ogie Omorose**
- LinkedIn: [Ogie Omorose](https://linkedin.com/in/ogie-omorose)

## Badges
[![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.2-00BFFF.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.36-blueviolet.svg)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-1.14.0-darkgreen.svg)](https://alembic.sqlalchemy.org/)
[![Database](https://img.shields.io/badge/Database-MySQL%2FPostgreSQL-orange.svg)](https://www.mysql.com/)
[![Cloudinary](https://img.shields.io/badge/Cloudinary-Integrated-blue.svg)](https://cloudinary.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/NewGenesis04/Blog-API-FastAPI/blob/main/LICENSE)

[![Readme was generated by Dokugen](https://img.shields.io/badge/Readme%20was%20generated%20by-Dokugen-brightgreen)](https://www.npmjs.com/package/dokugen)