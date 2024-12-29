--after insert on Buyer
--create a default bookmark list for them
CREATE OR REPLACE FUNCTION create_bookmark_list_on_first_login()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO BookmarkList (user_id, list_name)
  VALUES (NEW.user_id, 'Default');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_create_bookmark_list_on_first_login
AFTER INSERT ON Buyer
FOR EACH ROW
EXECUTE FUNCTION create_bookmark_list_on_first_login();
