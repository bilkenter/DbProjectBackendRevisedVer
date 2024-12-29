--view for admin for them to see all users
--can use with group by 'role' to have system overview
--no filtering required for this
CREATE OR REPLACE VIEW active_users AS
SELECT
  ua.user_id,
  ua.username,
  CASE
    WHEN EXISTS (SELECT 1 FROM AdminAccount WHERE user_id = ua.user_id) THEN 'Admin' --Mark admins
    WHEN EXISTS (SELECT 1 FROM Moderator WHERE user_id = ua.user_id) THEN 'Moderator' --Mark mods
    WHEN EXISTS (SELECT 1 FROM Ad WHERE user_id = ua.user_id) THEN 'Seller' --mark seller if a user has at least one ad
    WHEN EXISTS (SELECT 1 FROM PriceOffer WHERE user_id = ua.user_id) THEN 'Buyer' --mark buyer if a user has at least one offer made
    ELSE 'Inactive' --mark others as inactive
  END AS role
FROM
  UserAccount ua;
