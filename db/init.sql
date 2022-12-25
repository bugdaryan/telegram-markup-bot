CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

INSERT INTO users (id, username, password_hash, points, is_admin) VALUES
(uuid_generate_v4(), 'admin', 'pbkdf2:sha256:260000$7SzoT7HQXf9Xf6TE$dd9c61baa0865ab5c57eec4981b041a5e2bd31e66c50d84f320fc2f4e03af415', 0, true) ON CONFLICT DO NOTHING;