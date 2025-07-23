COMMENT_CREATE = """
Adds comment to a blog post.
- **blog_id** (path): Target blog ID
- **content** (body): Comment text
- **Returns**: Created comment with timestamp
"""

COMMENT_LIKE = """
Likes a comment (one like per user).
- **comment_id** (path): Target comment ID
- **Returns**: Updated like count
- **Errors**: 400 if already liked
"""

COMMENT_GET_ALL = """
Lists comments for a blog.
- **blog_id** (path): Target blog ID
- **include_all** (query): Show all comments (admin only)
- **author_id** (query): Filter by commenter
- **Returns**: Paginated comment list
"""

COMMENT_UPDATE = """
Edits comment content (owner only).
- **comment_id** (path): Comment ID
- **content** (body): New text
- **Returns**: Updated comment
"""

COMMENT_DELETE = """
Deletes comment (owner/admin).
- **comment_id** (path): Comment ID  
- **Returns**: Confirmation
- **Effects**: Removes from DB permanently
"""