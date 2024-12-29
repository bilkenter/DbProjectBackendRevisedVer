--view for admins to see report metrics
--for each report reason how many reports are out there
--see how many of the unique vehicles on the system are reported
--for each reason calculate the percentage attributed to them wrt total reports
--no filtering needed
CREATE OR REPLACE VIEW report_metrics AS
SELECT
  report_reason,
  COUNT(report_id) AS reports_count,
  COUNT(DISTINCT ad_id) AS unique_vehicles_reported,
  ROUND(100.0 * COUNT(report_id) / SUM(COUNT(report_id)) OVER (), 2) AS percentage_of_total_reports
FROM
  Report
GROUP BY
  report_reason;
