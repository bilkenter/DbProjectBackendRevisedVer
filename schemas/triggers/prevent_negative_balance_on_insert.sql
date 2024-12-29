--before insert on bank account
--prevent negative balance
CREATE OR REPLACE FUNCTION prevent_negative_balance_on_insert()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.account_balance < 0 THEN
    RAISE EXCEPTION 'Account balance cannot be negative.';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_negative_balance_on_insert
BEFORE INSERT ON BankAccount
FOR EACH ROW
EXECUTE FUNCTION prevent_negative_balance_on_insert();
