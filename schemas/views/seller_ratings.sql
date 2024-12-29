--can be used for every role
--for seller to see his rating
--for buyer to see sellers with higher or lower ratings and act accordingly
--for mods and admin to see the ratings and act if needed
CREATE OR REPLACE VIEW seller_ratings AS
SELECT
  s.user_id AS seller_id, --can use this to filter for seller but not buyer
  COALESCE(AVG(r.rating), 0) AS average_rating, --null handling
  COUNT(r.rating) AS review_count
FROM
  Review r
JOIN
  Seller s
    ON r.seller_id = s.user_id
GROUP BY
  s.user_id;
