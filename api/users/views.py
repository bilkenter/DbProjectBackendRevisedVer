# users/views.py
from psycopg2.extras import RealDictCursor
import bcrypt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .db_utils import get_connection
import json

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            email = data['email']
            #phone_number = data['phone_number']
            user_type = data['userType']
            notificationPreference = data['notificationPreference']

            # Validate inputs
            """if not username or not password or not email or not phone_number or not user_type or not notification_preferences:"""
            if not username or not password or not email or not user_type or not notificationPreference:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # Hash the password using bcrypt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insert user into the database
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    # Insert into UserAccount table
                    cursor.execute("""
                        INSERT INTO UserAccount (username, pass, email)
                        VALUES (%s, %s, %s)
                        RETURNING user_id;
                    """, (username, hashed_password.decode('utf-8'), email))  # store the hashed password as string
                    new_user_id = cursor.fetchone()[0]

                    # Insert into AppUser table for all users
                    cursor.execute("""
                        INSERT INTO AppUser (user_id, notification_preference)
                        VALUES (%s, %s);
                    """, (new_user_id, notificationPreference))

                    # Add user type relationship
                    if user_type == "Admin":
                        cursor.execute("""
                            INSERT INTO AdminAccount (user_id) 
                            VALUES (%s);
                        """, (new_user_id,))
                    elif user_type == "Moderator":
                        cursor.execute("""
                            INSERT INTO Moderator (user_id)
                            VALUES (%s);
                        """, (new_user_id,))
                    elif user_type == "Buyer":
                        cursor.execute("""
                            INSERT INTO Buyer (user_id)
                            VALUES (%s);
                        """, (new_user_id,))
                    elif user_type == "Seller":
                        cursor.execute("""
                            INSERT INTO Seller (user_id)
                            VALUES (%s);
                        """, (new_user_id,))
                    else:
                        return JsonResponse({'error': 'Invalid user type'}, status=400)

                    conn.commit()

            return JsonResponse({'message': 'User registered successfully', 'user_id': new_user_id}, status=201)

        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data['email']
            password = data['password']

            # Validate inputs
            if not email or not password:
                return JsonResponse({'error': 'Missing username or password'}, status=400)

            # Check credentials
            with get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT user_id, username, email, pass
                        FROM UserAccount
                        WHERE email = %s;
                    """, (email,))
                    user = cursor.fetchone()

            if user:
                # Verify the password
                if bcrypt.checkpw(password.encode('utf-8'), user['pass'].encode('utf-8')):
                    return JsonResponse({'message': 'Login successful', 'user': user}, status=200)
                else:
                    return JsonResponse({'error': 'Invalid credentials'}, status=401)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def create_vehicle_ad(request):
    if request.method == 'POST':
        try:
            # Parse incoming data from JSON
            data = json.loads(request.body)
            print(f"Received Data: {data}")

            # Extracting the values from the parsed data
            brand = data.get('brand')
            model_name = data.get('model_name')
            year = data.get('year')
            mileage = data.get('mileage')
            motor_power = data.get('motor_power')
            fuel_type = data.get('fuel_type')
            fuel_tank_capacity = data.get('fuel_tank_capacity')
            transmission_type = data.get('transmission_type')
            body_type = data.get('body_type')
            color = data.get('color')
            price = data.get('price')
            location = data.get('location')
            description = data.get('description')
            user_id = data.get('user_id')
            vehicle_type = data.get('vehicle_type')

            # Validate required fields
            if not all([brand, model_name, year, mileage, motor_power, price, location, description, vehicle_type]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # Proceed with inserting the data into the database
            # Insert into Vehicle table
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Vehicle (brand, model_name, year, mileage, motor_power, fuel_type, fuel_tank_capacity,
                                             transmission_type, body_type, color)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING vehicle_id;
                    """, (brand, model_name, year, mileage, motor_power, fuel_type, fuel_tank_capacity, transmission_type,
                          body_type, color))
                    vehicle_id = cursor.fetchone()[0]

                    # Insert additional vehicle data depending on vehicle type
                    if vehicle_type == "Car":
                        num_of_doors = data.get('numOfDoors')
                        cursor.execute("""
                            INSERT INTO Car (vehicle_id, number_of_doors)
                            VALUES (%s, %s);
                        """, (vehicle_id, num_of_doors))

                    # Insert ad into Ad table
                    cursor.execute("""
                        INSERT INTO Ad (user_id, vehicle_id, price, location, description)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING ad_id;
                    """, (user_id, vehicle_id, price, location, description))
                    ad_id = cursor.fetchone()[0]
                    conn.commit()

            return JsonResponse({'message': 'Vehicle ad created successfully', 'ad_id': ad_id}, status=201)

        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

@csrf_exempt
def get_all_cars(request):
    if request.method == 'GET':
        try:
            # Query the database to get car ads
            with get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT
                            ad.ad_id,
                            ad.price,
                            ad.location,
                            ad.description,
                            ad.posting_date,
                            vehicle.brand,
                            vehicle.model_name,
                            vehicle.year,
                            vehicle.mileage,
                            vehicle.motor_power,
                            vehicle.fuel_type,
                            vehicle.fuel_tank_capacity,
                            vehicle.transmission_type,
                            vehicle.body_type,
                            vehicle.color
                        FROM Ad ad
                        JOIN Vehicle vehicle ON ad.vehicle_id = vehicle.vehicle_id
                        WHERE ad.status = 'available';
                    """)
                    cars = cursor.fetchall()

            if cars:
                return JsonResponse({'cars': cars}, status=200)
            else:
                return JsonResponse({'cars': []}, status=200)  # Return empty array


        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

@csrf_exempt
def get_all_users(request):
    if request.method == 'GET':
        try:
            with get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    # Query to get all users with their type, notification preference, and if they are a seller, their car IDs
                    cursor.execute("""
                        SELECT u.user_id, u.username, u.email, a.notification_preference, 
                               CASE 
                                   WHEN s.user_id IS NOT NULL THEN 'Seller' 
                                   WHEN b.user_id IS NOT NULL THEN 'Buyer'
                                   WHEN m.user_id IS NOT NULL THEN 'Moderator'
                                   WHEN admin.user_id IS NOT NULL THEN 'Admin'
                                   ELSE 'Unknown'
                               END AS user_type,
                               COALESCE(array_agg(v.vehicle_id), '{}'::int[]) AS car_ids
                        FROM UserAccount u
                        LEFT JOIN AppUser a ON u.user_id = a.user_id
                        LEFT JOIN Seller s ON u.user_id = s.user_id
                        LEFT JOIN Buyer b ON u.user_id = b.user_id
                        LEFT JOIN Moderator m ON u.user_id = m.user_id
                        LEFT JOIN AdminAccount admin ON u.user_id = admin.user_id
                        LEFT JOIN Ad ad ON u.user_id = ad.user_id
                        LEFT JOIN Vehicle v ON ad.vehicle_id = v.vehicle_id
                        GROUP BY u.user_id, a.notification_preference, s.user_id, b.user_id, m.user_id, admin.user_id;
                    """)
                    users = cursor.fetchall()

            if users:
                return JsonResponse({'users': users}, status=200)
            else:
                return JsonResponse({'message': 'No users found'}, status=404)

        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def get_user_data(request):
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id')  # Retrieve user_id from query parameter
            
            # Handle missing user_id
            if not user_id:
                return JsonResponse({'error': 'User ID is required'}, status=400)

            # Fetch user data from the database
            with get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT username, email, user_id
                        FROM UserAccount
                        WHERE user_id = %s;
                    """, (user_id,))
                    user = cursor.fetchone()

            if user:
                return JsonResponse({'user': user}, status=200)
            else:
                return JsonResponse({'error': 'User not found'}, status=404)

        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def get_seller_ads(request):
    if request.method == 'GET':
        try:
            # Get user_id from the query parameters
            user_id = request.GET.get('user_id')  # Use GET to extract the query parameter
            print(f"Received Data: {user_id}")

            if not user_id:
                return JsonResponse({'error': 'User ID is required'}, status=400)

            with get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    # Query the seller_ads view to get the seller's ads
                    cursor.execute("""
                        SELECT * FROM seller_ads
                        WHERE seller_id = %s;
                    """, (user_id,))
                    ads = cursor.fetchall()
                    print(f"Received Data: {ads}")

            if ads:
                return JsonResponse({'ads': ads}, status=200)
            else:
                # Return an empty list when no ads are found
                return JsonResponse({'ads': []}, status=200)

        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def delete_ad(request, ad_id):
    if request.method == 'DELETE':
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    # Delete the ad from the Ad table
                    cursor.execute("""
                        DELETE FROM Ad
                        WHERE ad_id = %s
                        RETURNING ad_id;
                    """, (ad_id,))
                    deleted_ad = cursor.fetchone()

            if deleted_ad:
                return JsonResponse({'message': 'Ad deleted successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Ad not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
