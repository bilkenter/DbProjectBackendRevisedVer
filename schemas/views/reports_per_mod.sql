--admin view for tracking mod activity for each mod
CREATE OR REPLACE VIEW reports_per_mod AS
SELECT
  r.moderator_id, --can be used to filter a specific mod or not to see all mods
  ua.username AS moderator_username,
  COUNT(r.report_id) AS total_reports_managed,
  SUM(CASE WHEN r.status = 'resolved' THEN 1 ELSE 0 END) AS resolved_reports
FROM
  Report r
JOIN
  UserAccount ua
    ON r.moderator_id = ua.user_id
GROUP BY
  r.moderator_id, ua.username;
