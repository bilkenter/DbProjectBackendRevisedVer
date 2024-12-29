--mod view to see reports that are opened but not resolved or closed
CREATE OR REPLACE VIEW reported_listings AS
SELECT
  r.report_id,
  r.ad_id,
  a.user_id AS seller_id, --for filtering
  r.report_reason,
  r.reporter_id,
  ua.username AS reporter_username,
  r.report_date
FROM
  Report r
JOIN
  Ad a
    ON r.ad_id = a.ad_id
JOIN
  UserAccount ua
    ON r.reporter_id = ua.user_id
WHERE
  r.report_status = 'open';
