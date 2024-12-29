--view for buyer to see his bookmark
SELECT
  b.user_id AS buyer_id, --for filter
  a.ad_id,
  v.brand,
  v.model_name,
  v.year,
  a.price,
  a.status,
  a.posting_date,
  a.user_id AS seller_id,
  a.location
FROM
  BookmarkList b
JOIN
  Ad a
    ON b.ad_id = a.ad_id
JOIN
  Vehicle v
    ON a.vehicle_id = v.vehicle_id;
