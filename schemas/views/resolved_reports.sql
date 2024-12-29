--view for mod to see reports in resolved status
SELECT
  r.report_id,
  r.ad_id,
  v.brand,
  v.model_name,
  a.location,
  r.report_reason,
  r.moderator_id,--for filter
  r.resolution_date,
  r.resolution_note
FROM
  Report r
JOIN
  Ad a
    ON r.ad_id = a.ad_id
JOIN
  Vehicle v
    ON a.vehicle_id = v.vehicle_id
WHERE
  r.report_status = 'resolved';
