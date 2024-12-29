-- after updating an offer to be accepted
-- set ad status to closed
CREATE OR REPLACE FUNCTION update_ad_status_on_offer_accept()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.offer_status = 'accepted' THEN
    UPDATE Ad
    SET status = 'closed'
    WHERE ad_id = NEW.ad_id;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_ad_status_on_offer_accept
AFTER UPDATE ON PriceOffer
FOR EACH ROW
WHEN (OLD.offer_status IS DISTINCT FROM NEW.offer_status)
EXECUTE FUNCTION update_ad_status_on_offer_accept();
