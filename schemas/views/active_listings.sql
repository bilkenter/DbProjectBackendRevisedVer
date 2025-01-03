CREATE OR REPLACE VIEW active_listings AS
SELECT
  a.ad_id,
  a.user_id AS seller_id,  -- Filtering when used for seller, not buyer and admin
  v.vehicle_id,
  v.brand,
  v.model_name,
  v.year,
  a.status,
  a.price,
  a.location,
  v.mileage,
  v.motor_power,
  v.fuel_type,
  v.fuel_tank_capacity,
  v.transmission_type,
  v.body_type,
  v.color,
  a.description,
  -- Convert the BYTEA image data to base64 and use it
  COALESCE(array_agg('data:image/jpeg;base64,' || encode(i.image_data, 'base64')), '{}'::text[]) AS image_urls,
  'data:expert_reports/pdf;base64,' || encode(erp.pdf_data, 'base64') AS pdf,
  a.posting_date,
  ua.username AS seller_name,
  ua.email AS seller_email,
  v.vehicle_type,
  c.number_of_doors,
  m.wheel_number,
  m.cylinder_volume,
  m.has_basket,
  va.seat_number,
  va.roof_height,
  va.cabin_space,
  va.has_sliding_door
FROM
  Ad a
JOIN
  Vehicle v
    ON a.vehicle_id = v.vehicle_id
LEFT JOIN
  Image i
    ON a.ad_id = i.ad_id
LEFT JOIN
  Car c
    ON v.vehicle_id = c.vehicle_id
LEFT JOIN
  Motorcycle m
    ON v.vehicle_id = m.vehicle_id
LEFT JOIN
  Van va
    ON v.vehicle_id = va.vehicle_id
JOIN
  AppUser au
    ON a.user_id = au.user_id
JOIN
  UserAccount ua
    ON au.user_id = ua.user_id
LEFT JOIN
  ExpertReport erp
    ON erp.ad_id = a.ad_id
WHERE
  a.status = 'available'
GROUP BY
  a.ad_id, a.user_id, v.brand, v.vehicle_id, v.model_name, v.year, a.price, a.location, v.mileage,
  v.motor_power, v.fuel_type, v.transmission_type, v.body_type, v.color, a.description, a.posting_date, ua.username, ua.email, 
  c.vehicle_id, m.vehicle_id, va.vehicle_id, erp.pdf_data, v.vehicle_type;
