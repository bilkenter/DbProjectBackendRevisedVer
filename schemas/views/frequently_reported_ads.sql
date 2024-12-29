--view for mods to see ads that are most probably problematic
--can specify a frequency value to see the reported ads above a threshold
CREATE OR REPLACE VIEW frequently_reported_ads AS
SELECT
  r.ad_id,
  COUNT(r.report_id) AS total_reports
FROM
  Report r
WHERE
  r.status = 'open'
GROUP BY
  r.ad_id;
