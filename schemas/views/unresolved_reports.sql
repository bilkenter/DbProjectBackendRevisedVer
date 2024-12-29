--mod view for reports that are waiting to be resolved
--can also be used for admin to see distribution of reports to mods
CREATE OR REPLACE VIEW unresolved_reports AS
SELECT
  r.report_id,
  r.ad_id,
  a.location AS ad_location,
  v.brand AS vehicle_brand,
  v.model_name AS vehicle_model,
  r.report_reason,
  r.status,
  r.report_date,
  r.moderator_id, --can be used for admins and mods to filter mods
  ua.username AS moderator_username
FROM
  Report r
JOIN
  Ad a
    ON r.ad_id = a.ad_id
JOIN
  Vehicle v
    ON a.vehicle_id = v.vehicle_id
JOIN
  UserAccount ua
    ON r.moderator_id = ua.user_id
WHERE
  r.status IN ('open', 'in_progress');
