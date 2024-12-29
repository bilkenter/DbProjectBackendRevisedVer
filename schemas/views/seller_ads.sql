--view for seller to see all of their ads
CREATE OR REPLACE VIEW seller_ads AS
SELECT
  a.ad_id,
  a.user_id AS seller_id, --for filtering
  v.brand,
  v.model_name,
  v.year,
  a.price,
  v.mileage,
  a.status,
  a.location,
  a.description,
  a.posting_date
FROM
  Ad a
JOIN
  Vehicle v
    ON a.vehicle_id = v.vehicle_id;
