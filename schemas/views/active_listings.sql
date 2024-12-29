--primary view for sellers and buyers but can also be used for admins
--buyer to see all active listings that are flagged available
--also for seller to see their active ads
--can also be used for admins to see all active listings
CREATE OR REPLACE VIEW active_listings AS
SELECT
  a.ad_id,
  a.user_id AS seller_id, --filtering when used for seller not buyer and admin
  v.brand,
  v.model_name,
  v.year,
  a.price,
  a.location,
  v.mileage,
  v.motor_power,
  v.fuel_type,
  v.transmission_type,
  v.body_type,
  v.color,
  a.description,
  i.url AS image_url,
  a.posting_date
FROM
  Ad a
JOIN
  Vehicle v
    ON a.vehicle_id = v.vehicle_id
LEFT JOIN
  Image i
    ON a.ad_id = i.ad_id
WHERE
  a.status = 'available';
