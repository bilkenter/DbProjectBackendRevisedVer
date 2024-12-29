-- before updating a report as resolved
-- set resolution date to current date
CREATE OR REPLACE FUNCTION set_report_resolution_date_on_closure()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.report_status = 'resolved' THEN NEW.resolution_date := CURRENT_DATE;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_set_report_resolution_date_on_closure
BEFORE UPDATE ON Report
FOR EACH ROW
WHEN (OLD.report_status IS DISTINCT FROM NEW.report_status)
EXECUTE FUNCTION set_report_resolution_date_on_closure();
