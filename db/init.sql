CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

INSERT INTO users (id, username, password_hash, points, is_admin) VALUES
(uuid_generate_v4(), 'SAITAMA', 'pbkdf2:sha256:260000$joJByQ0nx4he67K0$ee8be18f5df94bbbadbcf5817cce73e006b4afb1d8691cc0899b475d918b523b', 0, true) ON CONFLICT DO NOTHING;