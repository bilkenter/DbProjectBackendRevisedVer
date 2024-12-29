--mod and admin view to see specific user's report history
CREATE OR REPLACE VIEW user_report_history AS
SELECT
  r.reporter_id, --for filtering
  ua.username AS reporter_username,
  COUNT(r.report_id) AS reports_count
FROM
  Report r
JOIN
  UserAccount ua
    ON r.reporter_id = ua.user_id
GROUP BY
  r.reporter_id, ua.username;
