--admin view for seeing mods activities
--see both resolved and unresolved reports for each mod
CREATE OR REPLACE VIEW moderator_performance AS
SELECT
  r.moderator_id,
  ua.username AS moderator_username,
  COUNT(CASE WHEN r.status = 'resolved' THEN 1 END) AS resolved_reports,
  COUNT(CASE WHEN r.status != 'resolved' THEN 1 END) AS unresolved_reports
FROM
  Report r
JOIN
  UserAccount ua
    ON r.moderator_id = ua.user_id
GROUP BY
  r.moderator_id, ua.username;
