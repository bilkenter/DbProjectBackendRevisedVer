--view for sellers all offers that are in pending state
CREATE OR REPLACE VIEW pending_offers AS
SELECT
  o.offer_id,
  o.ad_id,
  v.brand,
  v.model_name,
  o.offered_price,
  o.offer_status,
  o.user_id --for filtering
FROM
  PriceOffer o
JOIN
  Ad a
    ON o.ad_id = a.ad_id
JOIN
  Vehicle v
    ON a.vehicle_id = v.vehicle_id
WHERE
  o.offer_status = 'pending';
