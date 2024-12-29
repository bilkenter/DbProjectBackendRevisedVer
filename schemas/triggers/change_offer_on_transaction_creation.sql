--after insert on Transaction
--update the corresponding price offer status to be accepted
CREATE OR REPLACE FUNCTION change_offer_on_transaction_create()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE PriceOffer
  SET offer_status = 'accepted'
  WHERE offer_id = NEW.offer_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_change_offer_on_transaction_create
AFTER INSERT ON Transact
FOR EACH ROW
EXECUTE FUNCTION change_offer_on_transaction_create();
