-- after deleting an ad
-- automatically set report status to closed and add a resolution date and note
CREATE OR REPLACE FUNCTION close_report_on_ad_delete()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE Report
  SET status = 'closed',
    resolution_date = CURRENT_DATE,
    resolution_note = 'Ad deleted by seller'
  WHERE ad_id = OLD.ad_id;
  RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_close_reports_on_ad_deletion
AFTER DELETE ON Ad
FOR EACH ROW
EXECUTE FUNCTION close_report_on_ad_delete();

