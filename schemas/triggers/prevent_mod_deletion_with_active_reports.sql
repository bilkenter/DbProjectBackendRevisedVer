--if a mod has a report that is in open or in progress assigned to them
--prevent removal of that mod
CREATE OR REPLACE FUNCTION prevent_mod_deletion_with_active_reports()
RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM Report
    WHERE moderator_id = OLD.user_id AND status IN ('open', 'in_progress')
  ) THEN
    RAISE EXCEPTION 'Cannot delete moderator assigned to unresolved reports.';
  END IF;
  RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_moderator_deletion_with_active_reports
BEFORE DELETE ON Moderator
FOR EACH ROW
EXECUTE FUNCTION prevent_mod_deletion_with_active_reports();
