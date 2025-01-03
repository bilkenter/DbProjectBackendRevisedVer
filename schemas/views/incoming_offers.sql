--view for seller to see the incoming offers
--filter for seller_id to see specific seller's incoming offers
--it includes every offer meaning, the vehicle may be sold or not yet
CREATE OR REPLACE VIEW incoming_offers AS
SELECT
  o.offer_id,
  o.user_id AS buyer_id,
  ua.username AS buyer_username,
  o.offered_price,
  o.offer_status AS status,
  o.offer_date,
  a.ad_id,
  a.user_id AS seller_id, --for filtering
  v.brand,
  v.model_name,
  v.year,
  v.vehicle_id
FROM
  PriceOffer o
JOIN
  Ad a
    ON o.ad_id = a.ad_id
JOIN
  Vehicle v
    ON a.vehicle_id = v.vehicle_id
JOIN
  UserAccount ua
    ON o.user_id = ua.user_id;
