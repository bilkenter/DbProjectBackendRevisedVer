--admin view for seeing mods activities
--see both resolved and unresolved reports for each mod
SELECT
  r.moderator_id,
  ua.username AS moderator_username,
  COUNT(CASE WHEN r.report_status = 'resolved' THEN 1 END) AS resolved_reports,
  COUNT(CASE WHEN r.report_status != 'resolved' THEN 1 END) AS unresolved_reports
FROM
  Report r
JOIN
  UserAccount ua
    ON r.moderator_id = ua.user_id
GROUP BY
  r.moderator_id, ua.username;
