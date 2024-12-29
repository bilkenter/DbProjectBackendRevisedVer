-- before update on price offer
-- ensure no price update if its already accepted
CREATE OR REPLACE FUNCTION prevent_price_update_after_accept()
RETURNS TRIGGER AS $$
BEGIN
  IF OLD.offer_status = 'accepted' AND NEW.offered_price != OLD.offered_price THEN
    RAISE EXCEPTION 'Cannot update the price of an accepted offer.';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_offer_price_update_after_acceptance
BEFORE UPDATE ON PriceOffer
FOR EACH ROW
EXECUTE FUNCTION prevent_price_update_after_accept();
