/*
User has relation with:
  Admin: Parent Child
  Moderator: Parent Child
  AppUser: Parent Child
*/
CREATE TABLE IF NOT EXISTS UserAccount (
    user_id SERIAL,
    username VARCHAR(50) NOT NULL UNIQUE,
    pass VARCHAR(250) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY (user_id)
);

DO $$ BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'notification_preferences') THEN
       CREATE TYPE notification_preferences AS ENUM ('email', 'sms');
   END IF;
END $$;
CREATE TABLE IF NOT EXISTS AppUser (
    user_id INT NOT NULL,
    notification_preference notification_preferences DEFAULT 'email',
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES UserAccount(user_id) ON DELETE CASCADE
);

/*
Buyer has relation with:
  AppUser: Parent Child
  BookMarkList: One Buyer can have many BookMarkList
  PriceOffer: One Buyer can have many Price Offers
  Review: One Buyer can issue many Reviews
*/
CREATE TABLE IF NOT EXISTS Buyer (
    user_id INT NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES AppUser(user_id) ON DELETE CASCADE
);

/*
Seller has relation with:
  AppUser: Parent Child
  Ad: One Seller can have many Ads
  Review: One Seller can have many Reviews
*/
CREATE TABLE IF NOT EXISTS Seller (
    user_id INT NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES AppUser(user_id) ON DELETE CASCADE
);

/*
Admin has relation with:
  User: Parent Child
*/
CREATE TABLE IF NOT EXISTS AdminAccount (
    user_id INT NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES UserAccount(user_id) ON DELETE CASCADE
);

/*
Moderator has relation with:
  User: Parent Child
  ModerationAction: One Moderator can take many Moderation Action
  Ban: One Moderator can have many Bans
  Report: One Moderator can have many Reports assigned
*/
CREATE TABLE IF NOT EXISTS Moderator (
    user_id INT NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES UserAccount(user_id) ON DELETE CASCADE
);

/*
Vehicle has relation with:
  Ad: One Ad can only feature one Vehicle
*/
CREATE TABLE IF NOT EXISTS Vehicle(
  vehicle_id SERIAL,
  brand VARCHAR(30) NOT NULL,
  model_name VARCHAR(30) NOT NULL,
  year INT NOT NULL CHECK (year >= 1900),
  mileage INT NOT NULL CHECK(mileage >= 0),
  motor_power DECIMAL(5,2) CHECK (motor_power > 0),
  fuel_type VARCHAR(20),
  fuel_tank_capacity DECIMAL(5,2),
  transmission_type VARCHAR(20),
  body_type VARCHAR(20),
  color VARCHAR(20),
  PRIMARY KEY (vehicle_id)
);

/*
Car has relation with:
  Vehicle: Parent Child
*/
CREATE TABLE IF NOT EXISTS Car(
  vehicle_id INT NOT NULL,
  number_of_doors INT NOT NULL CHECK(number_of_doors >= 2 AND number_of_doors <= 6), -- not sure though
  PRIMARY KEY (vehicle_id),
  FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id) ON DELETE CASCADE
);

/*
Motorcycle has relation with:
  Vehicle: Parent Child
*/
CREATE TABLE IF NOT EXISTS Motorcycle(
  vehicle_id INT NOT NULL,
  wheel_number INT NOT NULL,
  cylinder_volume DECIMAL(5,2) CHECK (cylinder_volume > 0),
  has_basket BIT DEFAULT B'0',
  PRIMARY KEY (vehicle_id),
  FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id) ON DELETE CASCADE
);

/*
Van has relation with:
  Vehicle: Parent Child
*/
CREATE TABLE IF NOT EXISTS Van(
  vehicle_id INT NOT NULL,
  seat_number INT NOT NULL CHECK (seat_number >= 2 AND seat_number <= 32),
  roof_height DECIMAL(5,2) CHECK (roof_height > 0),
  cabin_space DECIMAL(5,2) CHECK (cabin_space > 0),
  has_sliding_door BIT DEFAULT B'0',
  PRIMARY KEY (vehicle_id),
  FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id) ON DELETE CASCADE
);


/*
Ad has relation with:
  Vehicle: One Ad can be associated with one Vehicle
  Expert Report: Weak Strong Entity relation, One Ad can have many Expert Reports
  Image: Weak Strong Entity relation, One Ad can have many Images
  Seller: One Seller can have many Ads
  Price Offer: One Ad can receive many Price Offers
  BookMarkList: Many Ads can reside at Many BookMarkLists ONLY MANY TO MANY RELATION IN SCHEMA
  Report: One Ad can receive many Reports
*/
DO $$ BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'ad_status') THEN
       CREATE TYPE ad_status AS ENUM ('available', 'closed');
   END IF;
END $$;

CREATE TABLE IF NOT EXISTS Ad(
  ad_id SERIAL,
  user_id INT NOT NULL,
  vehicle_id INT NOT NULL,
  price DECIMAL(10,2) NOT NULL CHECK(price > 0),
  location VARCHAR(100) NOT NULL,
  description TEXT NOT NULL,
  posting_date DATE DEFAULT CURRENT_TIMESTAMP,
  status ad_status DEFAULT 'available',
  PRIMARY KEY(ad_id),
  FOREIGN KEY(user_id) REFERENCES AppUser(user_id) ON DELETE CASCADE,
  FOREIGN KEY(vehicle_id) REFERENCES Vehicle(vehicle_id) ON DELETE CASCADE
);


DO $$ BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'status_type') THEN
       CREATE TYPE status_type AS ENUM ('pending', 'accepted', 'rejected');
   END IF;
END $$;
/*
PriceOffer has relation with:
  Transaction: One Price Offer for one Transaction
  Buyer: One Buyer offers many PriceOffers
  Ad: One Ad can receive many PriceOffers
*/
CREATE TABLE IF NOT EXISTS PriceOffer (
    offer_id SERIAL,
    user_id INT NOT NULL,
    ad_id INT NOT NULL,
    offered_price DECIMAL(11, 2) NOT NULL CHECK (offered_price > 0),
    offer_date DATE DEFAULT CURRENT_TIMESTAMP,
    offer_status status_type DEFAULT 'pending',
    PRIMARY KEY (offer_id),
    FOREIGN KEY (ad_id) REFERENCES Ad(ad_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Buyer(user_id) ON DELETE CASCADE
);

/*
BankAccount has relation with:
  AppUser: One AppUser can have many BankAccounts
  Transaction: One Transaction can be made from One Bank Account
*/
CREATE TABLE IF NOT EXISTS BankAccount (
    card_no VARCHAR(19) NOT NULL UNIQUE,
    user_id INT NOT NULL,
    iban VARCHAR(34) NOT NULL UNIQUE,
    owner_name VARCHAR(50) NOT NULL,
    exp_date DATE NOT NULL,
    cvc INT NOT NULL,
    account_balance DECIMAL(11, 2) NOT NULL CHECK (account_balance >= 0),
    PRIMARY KEY (card_no),
    FOREIGN KEY (user_id) REFERENCES AppUser(user_id) ON DELETE CASCADE
);

/*
Report has relation with:
  AppUser: One AppUser can issue many Reports
  Moderator: One moderator can manage many Reports
  ModerationAction: Many Moderation Actions can be reported about one Report
  Ad: Many Reports can be issued for one Ad
*/
DO $$ BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'report_status') THEN
       CREATE TYPE report_status AS ENUM ('open', 'in_progress', 'resolved', 'closed');
   END IF;
END $$;

CREATE TABLE IF NOT EXISTS Report(
  report_id SERIAL,
  moderator_id INT NOT NULL,
  ad_id INT NOT NULL,
  reporter_id INT NOT NULL,
  report_reason text NOT NULL,
  status report_status NOT NULL DEFAULT 'open',
  report_date DATE DEFAULT CURRENT_TIMESTAMP,
  resolution_date DATE NOT NULL,
  resolution_note text NOT NULL,
  PRIMARY KEY (report_id),
  FOREIGN KEY (moderator_id) REFERENCES UserAccount(user_id),
  FOREIGN KEY (ad_id) REFERENCES Ad(ad_id),
  FOREIGN KEY (reporter_id) REFERENCES AppUser(user_id)
);

/*
Transaction has relation with:---------------
  PriceOffer: One Price Offer can be paid for one Transaction
  BankAccount: One Transaction is made to one Bank Account(receiver)
  BankAccount: One Transaction is made to one Bank Account(sender)
*/
CREATE TABLE IF NOT EXISTS Transact (
    transaction_id SERIAL,
    offer_id INT NOT NULL,
    transaction_date DATE DEFAULT CURRENT_TIMESTAMP,
    receiver_card_no VARCHAR(19) NOT NULL,
    sender_card_no VARCHAR(19) NOT NULL,
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (offer_id) REFERENCES PriceOffer(offer_id) ON DELETE RESTRICT,
    FOREIGN KEY (receiver_card_no) REFERENCES BankAccount(card_no) ON DELETE RESTRICT,
    FOREIGN KEY (sender_card_no) REFERENCES BankAccount(card_no) ON DELETE RESTRICT
);

/*
Chat Room has relation with:
  AppUser: One chat room can only contain one Buyer,
  AppUser: One chat room can only contain one Seller
  Message: One ChatRoom can contain many Messages
*/
CREATE TABLE IF NOT EXISTS ChatRoom(
  chat_id SERIAL,
  buyer_id INT NOT NULL,
  seller_id INT NOT NULL,
  PRIMARY KEY (chat_id),
  FOREIGN KEY (buyer_id) REFERENCES AppUser(user_id),
  FOREIGN KEY (seller_id) REFERENCES AppUser(user_id)
);

/*
Message has relation with:
  AppUser: One message can be attributed to one AppUser (receiver or sender)
  AppUser: One message can be attributed to one AppUser (receiver or sender)
  Chat Room: One Chat Room can contain many Messages
*/
CREATE TABLE IF NOT EXISTS Message(
  message_id SERIAL,
  chat_id INT NOT NULL,
  sender_id INT NOT NULL,
  receiver_id INT NOT NULL,
  content TEXT NOT NULL,
  sent_date DATE DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (message_id, chat_id),
  FOREIGN KEY (chat_id) REFERENCES ChatRoom(chat_id),
  FOREIGN KEY (sender_id) REFERENCES AppUser(user_id),
  FOREIGN KEY (receiver_id) REFERENCES AppUser(user_id)
);



/*
Moderation Action has relation with:
  Moderator: One moderator can take many Moderation Actions
  Report: Many moderation actions can be reported about one Report
*/
DO $$ BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'action_status') THEN
       CREATE TYPE action_status AS ENUM ('pending', 'completed', 'revised');
   END IF;
END $$;

CREATE TABLE IF NOT EXISTS ModerationAction(
  action_id SERIAL,
  report_id INT NOT NULL,
  moderator_id INT NOT NULL,
  action_type VARCHAR(100) NOT NULL,
  status action_status NOT NULL DEFAULT 'pending',
  PRIMARY KEY (action_id),
  FOREIGN KEY (report_id) REFERENCES Report(report_id),
  FOREIGN KEY (moderator_id) REFERENCES UserAccount(user_id)
);

/*
Expert Report has relation with:
  Ad: Weak and Strong Entity, One Ad can contain many Expert Reports
*/
CREATE TABLE IF NOT EXISTS ExpertReport(
  report_id SERIAL,
  ad_id INT NOT NULL,
  report_date DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  expert_name VARCHAR(20) NOT NULL,
  PRIMARY KEY (ad_id, report_id),
  FOREIGN KEY (ad_id) REFERENCES Ad(ad_id)
);

/*
Image has relation with:
  Ad: Weak and Strong Entity, One Ad can contain many Images
*/
CREATE TABLE IF NOT EXISTS Image(
  image_id SERIAL,
  ad_id INT NOT NULL,
  url TEXT NOT NULL,
  PRIMARY KEY (ad_id, image_id),
  FOREIGN KEY (ad_id) REFERENCES Ad(ad_id)
);

/*
BookmarkList has relation with:
  AppUser: One AppUser can have many BookmarkLists
  Ad: Many Ads can exist in Many BookMarkLists (MANY TO MANY RELATION)
*/
CREATE TABLE IF NOT EXISTS BookmarkList(
  bookmark_id SERIAL,
  user_id INT NOT NULL,
  list_name VARCHAR(50) NOT NULL,
  PRIMARY KEY (bookmark_id),
  FOREIGN KEY (user_id) REFERENCES AppUser(user_id) ON DELETE CASCADE 
)


/*
Review has relation with:
  Buyer: One Buyer can issue many Reviews
  Seller: One Seller can have many Reviews
*/
CREATE TABLE IF NOT EXISTS Review(
  review_id SERIAL,
  reviewing_id INT NOT NULL,
  reviewed_id INT NOT NULL,
  rating INT NOT NULL CHECK(rating >= 1 AND rating <= 5),
  comment TEXT NOT NULL,
  review_date DATE DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (review_id),
  FOREIGN KEY (reviewing_id) REFERENCES Buyer(user_id) ON DELETE CASCADE,
  FOREIGN KEY (reviewed_id) REFERENCES Seller(user_id) ON DELETE CASCADE
);