CREATE EXTENSION pg_trgm;

CREATE TABLE images(
  id SERIAL PRIMARY KEY,
  vk VARCHAR(255) DEFAULT '_',
  vk_small VARCHAR(255) DEFAULT '_', 
  tg VARCHAR(255) DEFAULT '_',
  tg_small VARCHAR(255) DEFAULT '_',
  source_vk VARCHAR(255) DEFAULT '_'
);

CREATE TABLE texts(
  img_id SERIAL NOT NULL,
  text_ru TEXT DEFAULT '',
  text_en TEXT DEFAULT '',
  FOREIGN KEY (img_id) REFERENCES images(id)
);

CREATE TABLE users(
  id BIGINT PRIMARY KEY,
  lang CHAR(2)
);

CREATE TABLE actions(
  id SERIAL PRIMARY KEY,
  time TIMESTAMP NOT NULL,
  user_id BIGINT NOT NULL,
  img_id SERIAL,
  action CHAR(3) NOT NULL,
  detail JSON,
  FOREIGN KEY (img_id) REFERENCES images(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
