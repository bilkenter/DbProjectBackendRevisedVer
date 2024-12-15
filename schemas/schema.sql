create table SWUser 
(
    user_id SERIAL NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    pass VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY (user_id)
    --FOREIGN KEY (user_id) REFERENCES AppUser(user_id) ON DELETE CASCADE
);

CREATE TYPE notification_preferences AS ENUM ('email', 'sms');
CREATE TABLE AppUser 
(
    user_id INT NOT NULL,
    notification_preference notification_preferences DEFAULT 'email',
    iban VARCHAR(34) NOT NULL UNIQUE,
    balance DECIMAL(10, 2) NOT NULL CHECK (balance >= 0),
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES SWUser(user_id) ON DELETE CASCADE
);

CREATE TABLE Buyer 
(
    user_id INT NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES AppUser(user_id) ON DELETE CASCADE
);

CREATE TABLE Seller 
(
    user_id INT NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES AppUser(user_id) ON DELETE CASCADE
);

CREATE TABLE Admin 
(
    user_id INT NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES SWUser(user_id) ON DELETE CASCADE
);

CREATE TABLE  Moderator 
(
    user_id INT NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES SWUser(user_id) ON DELETE CASCADE
);

CREATE TYPE status_type AS ENUM ('pending', 'accepted', 'rejected');
CREATE TABLE  PriceOffer 
(
    offer_id SERIAL NOT NULL,
    user_id INT NOT NULL,
    ad_id INT NOT NULL,
    offered_price DECIMAL(11, 2) NOT NULL CHECK (offered_price > 0),
    offer_date DATE DEFAULT CURRENT_TIMESTAMP,
    offer_status status_type DEFAULT 'pending',
    PRIMARY KEY (offer_id),
    --FOREIGN KEY (ad_id) REFERENCES Ad(ad_id) ON DELETE CASCADE, -- TODO emirhan
    FOREIGN KEY (user_id) REFERENCES Buyer(user_id) ON DELETE CASCADE
);

CREATE TYPE payment_type AS ENUM ('bank_account', 'in_app_balance');
CREATE TABLE PaymentMethod 
(
    payment_id SERIAL NOT NULL,
    user_id INT NOT NULL,
    pay_type payment_type NOT NULL,
    card_no VARCHAR(19),
    PRIMARY KEY (payment_id, user_id),
    FOREIGN KEY (user_id) REFERENCES Buyer(user_id) ON DELETE CASCADE
);



CREATE TABLE  BankAccount 
(
    card_no VARCHAR(19) NOT NULL UNIQUE,
    user_id INT NOT NULL,
    iban VARCHAR(34) NOT NULL UNIQUE,   -- should it be unique? does it affect 2 people having the same iban? (like mother and child)
    owner_name VARCHAR(50) NOT NULL,
    exp_date DATE NOT NULL, -- this seems better bc makes comparisons easier (in 1 shot) but we can ask to TA if should it be a combination of month and year
    cvc INT NOT NULL,
    account_balance DECIMAL(11, 2) NOT NULL CHECK (account_balance >= 0),
    PRIMARY KEY (card_no),
    FOREIGN KEY (user_id) REFERENCES AppUser(user_id) ON DELETE CASCADE
);

ALTER TABLE PaymentMethod
ADD CONSTRAINT fk_card_no FOREIGN KEY (card_no) REFERENCES BankAccount(card_no) ON DELETE SET NULL;

CREATE FUNCTION chk_type_card_no() RETURNS TRIGGER
LANGUAGE plpgsql AS
$$
BEGIN
    IF (NEW.pay_type = 'app_balance' AND NEW.card_no IS NOT NULL) OR
       (NEW.pay_type = 'bank_account' AND NEW.card_no IS NULL) THEN
        RAISE EXCEPTION 'Invalid payment type and card number';
    END IF;
    RETURN NEW;
END;
$$;

CREATE CONSTRAINT TRIGGER chk_type_card_no
AFTER INSERT OR UPDATE ON PaymentMethod
FOR EACH ROW
EXECUTE FUNCTION chk_type_card_no();

CREATE TABLE Transact
(
    transaction_id SERIAL NOT NULL,
    payment_id INT NOT NULL,
    user_id INT NOT NULL,
    offer_id INT NOT NULL,
    transaction_date DATE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (payment_id, user_id) REFERENCES PaymentMethod(payment_id, user_id) ON DELETE RESTRICT, -- should it be null or cascade?
    FOREIGN KEY (offer_id) REFERENCES PriceOffer(offer_id) ON DELETE RESTRICT,
    FOREIGN KEY (user_id) REFERENCES Buyer(user_id) ON DELETE SET NULL
);

