CREATE TABLE IF NOT EXISTS User (
    user_id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES AppUser(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS AppUser (
    user_id INT NOT NULL,
    notification_preference ENUM('email', 'sms') DEFAULT 'email',
    iban VARCHAR(34) NOT NULL UNIQUE,
    balance DECIMAL(10, 2) NOT NULL CHECK (balance >= 0),
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Buyer (
    user_id INT NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES AppUser(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Seller (
    user_id INT NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES AppUser(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Admin (
    user_id INT NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Moderator (
    user_id INT NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);