-- before deleting an ad
-- ensure every offer made to it that is in pending state is rejected
CREATE OR REPLACE FUNCTION resolve_pending_offers_on_ad_delete()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE PriceOffer
  SET offer_status = 'rejected'
  WHERE ad_id = OLD.ad_id AND offer_status = 'pending';

  RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_resolve_pending_offers_on_ad_delete
BEFORE DELETE ON Ad
FOR EACH ROW
EXECUTE FUNCTION resolve_pending_offers_on_ad_delete();
