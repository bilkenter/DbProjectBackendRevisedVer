--view for sellers to see their ads that has not received any offers yet
CREATE OR REPLACE VIEW ads_without_offers AS
SELECT
  a.ad_id,
  a.user_id AS seller_id, --for filtering
  v.brand,
  v.model_name,
  v.year,
  a.price,
  a.posting_date
FROM
  Ad a
JOIN
  Vehicle v
    ON a.vehicle_id = v.vehicle_id
WHERE NOT EXISTS (
  SELECT 1
  FROM PriceOffer o
  WHERE o.ad_id = a.ad_id
);
