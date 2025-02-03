# Table of Contents

- [Introduction](#introduction)
- [Authentication and Authorization](#authentication-and-authorization)
- [User Management](#user-management)
- [Blog Management](#blog-management)
- [Follow Management](#follow-management)
- [Comment Management](#comment-management)
- [Pydantic Schemas](#pydantic-schemas)
- [Dependencies and Libraries](#dependencies-and-libraries)

# Introduction

This project is a FastAPI-based application designed to manage blogs, users, comments, and follow relationships. It includes features such as user authentication, role-based authorization, CRUD operations for blogs and comments, and the ability to follow/unfollow other users.

# Authentication and Authorization

The application uses JWT-based authentication with role-based access control. Users can have one of the following roles:

- **reader** : Can read blogs and create comments.
- **author** : Can create, update, and delete their own blogs and comments.
- **admin** : Has full control over all resources.

Endpoints requiring authentication are protected using **get_current_user**, while specific roles are enforced using **role_required**