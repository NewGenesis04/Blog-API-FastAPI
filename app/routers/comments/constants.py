COMMENT_ON_BLOG_REQUEST_LOG = (
    "comment_on_blog endpoint has been called for blog_id: {blog_id}"
)
GET_COMMENTS_REQUEST_LOG = (
    "get_comments endpoint has been called for blog_id: {blog_id}, include_all: {include_all}, author_id: {author_id}"
)
LIKE_COMMENT_REQUEST_LOG = "like_comment endpoint has been called for comment_id: {comment_id}"
UPDATE_COMMENT_REQUEST_LOG = "update_comment endpoint has been called for comment_id: {comment_id}"
DELETE_COMMENT_REQUEST_LOG = "delete_comment endpoint has been called for comment_id: {comment_id}"
UNLIKE_COMMENT_REQUEST_LOG = "unlike_comment endpoint has been called for comment_id: {comment_id}"