-- before inserting on review
-- ensure there are only one review submitted from buyer to seller
CREATE OR REPLACE FUNCTION prevent_duplicate_reviews()
RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM Review
    WHERE buyer_id = NEW.buyer_id AND seller_id = NEW.seller_id
  ) THEN
    RAISE EXCEPTION 'Duplicate review: A buyer can only submit one review per seller';
  END IF;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_duplicate_reviews
BEFORE INSERT ON Review
FOR EACH ROW
EXECUTE FUNCTION prevent_duplicate_reviews();
