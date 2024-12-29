-- after update of ad price
--when a price of an ad changes, reject the offers made to it
-- this is a helpful trigger for buyers
-- if they want to reject every offer made to an ad clearly they are not satisfied with the offers
-- so just change the ad price then it will reject all offers made to ad
CREATE OR REPLACE FUNCTION reject_offers_on_price_change()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE PriceOffer
  SET offer_status = 'rejected'
  WHERE ad_id = NEW.ad_id AND offer_status = 'pending';
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_reject_offers_on_price_change
AFTER UPDATE OF price ON Ad
FOR EACH ROW
EXECUTE FUNCTION reject_offers_on_price_change();
