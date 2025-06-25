CREATE INDEX ix_users_created_at ON users (created_at);

--@block
SHOW INDEXES FROM users;