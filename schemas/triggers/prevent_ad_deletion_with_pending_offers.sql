--before delete on ad
--prevent deletion if there is an unresolved offer associated with the ad
CREATE OR REPLACE FUNCTION prevent_ad_deletion_with_pending_offers()
RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM PriceOffer
    WHERE ad_id = OLD.ad_id AND offer_status = 'pending'
  ) THEN
    RAISE EXCEPTION 'Cannot delete ad with pending offers.';
  END IF;
  RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_ad_deletion_with_pending_offers
BEFORE DELETE ON Ad
FOR EACH ROW
EXECUTE FUNCTION prevent_ad_deletion_with_pending_offers();
