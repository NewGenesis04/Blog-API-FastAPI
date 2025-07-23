"""
Centralized API route descriptions for frontend developers.
"""

# Auth Routes
AUTH_LOGIN = """
Authenticates a user and returns JWT tokens.
- **identifier** (body): Email or username
- **password** (body): User's password
- **Returns**: {access_token, refresh_token, token_type: "bearer"}
- **Effects**: Starts authenticated session
"""

AUTH_LOGOUT = """
Revokes the current refresh token.
- **Requires**: Valid refresh token in Authorization header
- **Returns**: Confirmation message
- **Effects**: Invalidates refresh token immediately
"""

AUTH_REFRESH = """
Generates new access token using refresh token.
- **Requires**: Valid refresh token in Authorization header
- **Returns**: New access_token
- **Effects**: Extends session without re-login
"""

AUTH_REGISTER = """
Creates a new user account.
- **username** (body): 3-20 chars, unique
- **email** (body): Valid email, unique
- **password** (body): Min 8 chars
- **role** (body): Optional (default: "reader")
- **Returns**: Basic user profile
- **Effects**: New user record in DB
"""

AUTH_GET_ME = """
Returns the current authenticated user's profile.
- **Returns**: {id, username, email, role}
- **Effects**: No changes, just fetches profile
"""

AUTH_UPDATE_PASSWORD = """
Changes user password.
- **old_password** (body): Current password
- **new_password** (body): New password
- **Returns**: Success message
- **Effects**: Updates password hash
"""


# User Routes
USER_GET_ALL = """
Lists all users (admin-only).
- **Returns**: List of user summaries [id, username, email, profile_url, created_at, job_description]
"""

USER_GET_CURRENT_USER = """
Returns profile of the current or specified user.
- **altId** (query): Optional user ID to fetch (default: current user)
- **Returns**: Full user profile with blogs/comments if any
"""
USER_GET_BY_ID = """
Gets detailed user profile.
- **altId** (query): Optional user ID (default: current user)
- **Returns**: Full profile with blogs/comments/follows
"""
USER_DELETE = """
Deletes user account (irreversible).
- **Returns**: Confirmation message
- **Effects**: Removes user and all associated data
"""
USER_UPDATE = """
Updates user profile.
- **username** (body): New username (optional)
- **email** (body): New email (optional)
- **bio** (body): New bio text (optional)
- **job_description** (body): New job description (optional)
- **Returns**: Updated user profile
"""

# Blog Routes
BLOG_CREATE = """
Creates a new blog post.
- **title** (body): Post title (required)
- **content** (body): Markdown/content (required)
- **published** (body): Visibility flag (default: false)
- **tag** (body): Category tag (tech/lifestyle/etc.)
- **Returns**: Created blog with ID
"""

BLOG_GET_BY_TAG = """
Lists blogs filtered by tag.
- **tag** (path): Filter tag (e.g., 'technology')
- **Returns**: List of published blogs with this tag
"""

BLOG_GET_ALL = """
Lists blogs with optional filters.
- **user_id** (query): Filter by author ID
- **Returns**: List of blogs (published only for non-admins)
"""

BLOG_GET_CURRENT_USER = """
Gets blogs by current authenticated user.
- **Returns**: All blogs (including drafts) by this user
"""

BLOG_GET_BY_ID = """
Gets single blog post by ID.
- **id** (path): Blog ID  
- **Returns**: Full blog content with comments
- **Notes**: Drafts only visible to owner/admin
"""

BLOG_UPDATE = """
Updates blog post (author/admin only).
- **id** (path): Blog ID to update
- **title** (body): New title (optional)
- **content** (body): New content (optional)
- **published** (body): Change visibility
- **Returns**: Updated blog
"""

BLOG_DELETE = """
Deletes blog post (author/admin only).
- **id** (path): Blog ID to delete
- **Returns**: Confirmation message
- **Effects**: Cascades to comments
"""

# File Routes
FILE_GET_PROFILE_PIC = """
Gets the profile url from db
- **Returns**: {image_url: "https://..."}
"""

FILE_GET_COVER_PHOTO = """
Gets the cover_photo url from db
- **Returns**: {image_url: "https://..."}
"""

FILE_UPLOAD_PROFILE_PIC = """
Uploads profile picture (replaces existing).
- **file** (form-data): Image file (jpg/png < 5MB)
- **Returns**: {image_url: "https://..."}
- **Effects**: Deletes old picture from cloud
"""

FILE_DELETE_PROFILE_PIC = """
Removes user's profile picture.
- **Effects**: Clears profile_url, deletes from cloud
- **Returns**: Confirmation message
"""

FILE_UPLOAD_COVER_PHOTO = """
Uploads cover photo (replaces existing).
- **file** (form-data): Image file (jpg/png < 5MB)
- **Returns**: {image_url: "https://..."}
- **Effects**: Deletes old picture from cloud
"""

FILE_DELETE_COVER_PHOTO = """
Removes user's cover photo.
- **Effects**: Clears cover_photo_url, deletes from cloud
- **Returns**: Confirmation message
"""

# Follow Routes
FOLLOW_USER = """
Follows another user.
- **userId** (path): ID of user to follow
- **Returns**: Success message
- **Errors**: 400 if already following
"""

UNFOLLOW_USER = """
Stops following a user.
- **userId** (path): ID of user to unfollow
- **Returns**: Success message
- **Errors**: 400 if not currently following
"""

FOLLOW_GET_FOLLOWERS = """
Lists followers of a user.
- **alt_user** (query): Target user ID (default: current user)
- **Returns**: List of follower profiles
"""

FOLLOW_GET_FOLLOWING = """
Lists who a user follows.
- **alt_user** (query): Target user ID (default: current user)  
- **Returns**: List of followed user profiles
"""
