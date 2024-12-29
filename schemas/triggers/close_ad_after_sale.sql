--after insert on Transaction
--if a sale is done set ad status to closed
CREATE OR REPLACE FUNCTION close_ad_after_sale()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE Ad
  SET status = 'closed'
  WHERE ad_id = (SELECT ad_id FROM PriceOffer WHERE offer_id = NEW.offer_id);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--insert on transact implies an offer has been accepted
CREATE TRIGGER trg_close_ad_after_sale
AFTER INSERT ON Transact
FOR EACH ROW
EXECUTE FUNCTION close_ad_after_sale();
