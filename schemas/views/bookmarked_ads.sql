--view for buyer to see his bookmark
CREATE OR REPLACE VIEW bookmarked_ads AS
SELECT
  b.user_id AS buyer_id, --for filter
  bla.ad_id,
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
  BookmarkListAd bla
    ON b.bookmark_id = bla.bookmark_id
JOIN
  Ad a
    ON bla.ad_id = a.ad_id
JOIN
  Vehicle v
    ON a.vehicle_id = v.vehicle_id;
