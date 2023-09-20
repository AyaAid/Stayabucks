-- Création de la table "users"
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  role VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  isVerified BOOLEAN NOT NULL DEFAULT FALSE
);

-- Création de la table "drink"
CREATE TABLE drink (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  price FLOAT NOT NULL
);

-- Création de la table "supplement_type"
CREATE TABLE supplement_type (
  id SERIAL PRIMARY KEY,
  category VARCHAR(255) NOT NULL -- syrup, milk, other
);

-- Création de la table "supplement" avec référence à "supplement_type"
CREATE TABLE supplement (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  price FLOAT NOT NULL,
  type_id INTEGER NOT NULL REFERENCES supplement_type(id) ON DELETE CASCADE
);

-- Création de la table "drink_created"
CREATE TABLE drink_created (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  drink_id INTEGER NOT NULL REFERENCES drink(id) ON DELETE CASCADE
);

-- Création de la table "drink_supplement_association" (Many-to-Many)
CREATE TABLE drink_supplement_association (
  id SERIAL PRIMARY KEY,
  drink_id INTEGER NOT NULL REFERENCES drink(id) ON DELETE CASCADE,
  supplement_id INTEGER NOT NULL REFERENCES supplement(id) ON DELETE CASCADE
);

-- Création de la table "drink_created_supplement_association" (Many-to-Many)
CREATE TABLE drink_created_supplement_association (
  id SERIAL PRIMARY KEY,
  drink_created_id INTEGER NOT NULL REFERENCES drink_created(id) ON DELETE CASCADE,
  supplement_id INTEGER NOT NULL REFERENCES supplement(id) ON DELETE CASCADE
);

-- Création de la table "drink_created_likes"
CREATE TABLE drink_created_likes (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  drink_created_id INTEGER NOT NULL REFERENCES drink_created(id) ON DELETE CASCADE
);

-- Suppression en cascade pour les "supplement" liés à un "supplement_type" supprimé
-- Suppression en cascade pour les "drink_supplement_association" liés à un "drink" supprimé
-- Suppression en cascade pour les "drink_created" liés à un "drink" supprimé
-- Suppression en cascade pour les "drink_created_supplement_association" liés à un "drink_created" supprimé
ALTER TABLE supplement_type
  ADD CONSTRAINT fk_supplement_type
  FOREIGN KEY (id)
  REFERENCES supplement(type_id)
  ON DELETE CASCADE;

ALTER TABLE drink
  ADD CONSTRAINT fk_drink
  FOREIGN KEY (id)
  REFERENCES drink_supplement_association(drink_id)
  ON DELETE CASCADE;

ALTER TABLE drink_created
  ADD CONSTRAINT fk_drink_created
  FOREIGN KEY (drink_id)
  REFERENCES drink(id)
  ON DELETE CASCADE;

ALTER TABLE drink_created_supplement_association
  ADD CONSTRAINT fk_drink_created_association
  FOREIGN KEY (drink_created_id)
  REFERENCES drink_created(id)
  ON DELETE CASCADE;
