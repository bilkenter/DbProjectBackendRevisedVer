--system overview for admin
CREATE OR REPLACE VIEW system_metrics AS
SELECT
  (SELECT COUNT(*) FROM UserAccount) AS total_users,
  (SELECT COUNT(*) FROM Ad WHERE status = 'available') AS active_ads,
  (SELECT COUNT(*) FROM Transact) AS total_transactions,
  (SELECT COUNT(*) FROM Report) AS total_reports;
