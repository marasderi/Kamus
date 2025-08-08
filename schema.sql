
-- Veritabanı oluşturma
CREATE DATABASE kamus;
-- Kullanıcı oluşturma
CREATE USER kamus WITH ENCRYPTED PASSWORD 'your_password_here';
GRANT ALL PRIVILEGES ON DATABASE kamus TO kamus;

-- Aşağıdaki tablolar 'kamus' veritabanı içinde oluşturulmalıdır

-- Kullanıcılar
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(100),
    avatar_url TEXT,
    bio VARCHAR(150),
    birth_date DATE,
    gender CHAR(1),
    city VARCHAR(100),
    education VARCHAR(100),
    workplace VARCHAR(100),
    profession VARCHAR(100),
    interests TEXT,
    social_links JSONB,
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    post_count INTEGER DEFAULT 0,
    role_id INTEGER REFERENCES roles(id),
    is_active BOOLEAN DEFAULT TRUE
);

-- Roller
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- Gönderiler
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    category_id INTEGER REFERENCES categories(id),
    is_visible BOOLEAN DEFAULT TRUE,
    is_candidate BOOLEAN DEFAULT FALSE,
    is_draft BOOLEAN DEFAULT FALSE
);

-- Yorumlar
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id),
    user_id INTEGER REFERENCES users(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Hikayeler
CREATE TABLE stories (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- Etiketler
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Gönderi-Etiket ilişkisi
CREATE TABLE post_tags (
    post_id INTEGER REFERENCES posts(id),
    tag_id INTEGER REFERENCES tags(id),
    PRIMARY KEY (post_id, tag_id)
);

-- Kategoriler
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

-- Gruplar
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

-- Kullanıcı-Gruplar ilişkisi
CREATE TABLE user_groups (
    user_id INTEGER REFERENCES users(id),
    group_id INTEGER REFERENCES groups(id),
    PRIMARY KEY (user_id, group_id)
);

-- Beğeniler
CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    post_id INTEGER REFERENCES posts(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Takip ilişkisi
CREATE TABLE follows (
    follower_id INTEGER REFERENCES users(id),
    following_id INTEGER REFERENCES users(id),
    PRIMARY KEY (follower_id, following_id)
);

-- Ayarlar
CREATE TABLE settings (
    user_id INTEGER PRIMARY KEY REFERENCES users(id),
    preferences JSONB,
    blocked_users INTEGER[],
    favorite_posts INTEGER[],
    display_categories INTEGER[]
);
