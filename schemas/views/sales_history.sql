--view for seller, self explanatory name
CREATE OR REPLACE VIEW sales_history AS
SELECT
  t.transaction_id,
  a.ad_id,
  a.user_id AS seller_id,
  o.user_id AS buyer_id,
  v.brand,
  v.model_name,
  a.location,
  t.transaction_date,
  o.offered_price
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
