--before update on Transaction
-- dont let any updates here because
-- transaction table is reserved for price offers that are accepted
-- we wont let any changes to transaction only inserts after an offer is accepted
CREATE OR REPLACE FUNCTION prevent_transaction_updates()
RETURNS TRIGGER AS $$
BEGIN
  RAISE EXCEPTION 'Transactions cannot be updated once created.';
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_transaction_updates
BEFORE UPDATE ON Transact
FOR EACH ROW
EXECUTE FUNCTION prevent_transaction_updates();
