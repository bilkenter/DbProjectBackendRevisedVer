-- Primary view for sellers, buyers, and admins to see active listings
CREATE OR REPLACE VIEW active_listings AS
SELECT
  a.ad_id,
  a.user_id AS seller_id,  -- Filtering when used for seller, not buyer and admin
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
  -- Convert the BYTEA image data to base64 and use it
  COALESCE(array_agg('data:image/jpeg;base64,' || encode(i.image_data, 'base64')), '{}'::text[]) AS image_urls,
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
  a.status = 'available'
GROUP BY
  a.ad_id, a.user_id, v.brand, v.model_name, v.year, a.price, a.location, v.mileage,
  v.motor_power, v.fuel_type, v.transmission_type, v.body_type, v.color, a.description, a.posting_date;