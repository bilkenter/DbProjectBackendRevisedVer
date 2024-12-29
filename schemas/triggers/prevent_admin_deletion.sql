--before delete on admin
--prevent deleting admin all together so there is always one admin in the system
CREATE OR REPLACE FUNCTION prevent_admin_account_deletion()
RETURNS TRIGGER AS $$
BEGIN
  RAISE EXCEPTION 'Admin accounts cannot be deleted.';
  RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_admin_account_deletion
BEFORE DELETE ON AdminAccount
FOR EACH ROW
EXECUTE FUNCTION prevent_admin_account_deletion();
