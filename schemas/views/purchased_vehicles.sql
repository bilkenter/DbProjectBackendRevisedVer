--buyer view to track their purchase history
CREATE OR REPLACE VIEW purchased_vehicles AS
SELECT
  o.user_id AS buyer_id, --for filtering
  o.offered_price AS price,
  v.brand,
  v.model_name,
  t.transaction_date AS purchase_date
FROM
  Transact t
JOIN
  PriceOffer o
    ON t.offer_id = o.offer_id
JOIN
  Ad a
    ON o.ad_id = a.ad_id
JOIN
  Vehicle v
    ON a.vehicle_id = v.vehicle_id;
