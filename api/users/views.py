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
            data = json.loads(request.body)
            brand = data['brand']
            model_name = data['model_name']
            year = data['year']
            mileage = data['mileage']
            motor_power = data['motor_power']
            fuel_type = data['fuel_type']
            fuel_tank_capacity = data['fuel_tank_capacity']
            transmission_type = data['transmission_type']
            body_type = data['body_type']
            color = data['color']
            price = data['price']
            location = data['location']
            description = data['description']
            user_id = data['user_id']  # The logged-in seller's user_id
            
            # Validate required fields
            if not all([brand, model_name, year, mileage, motor_power, price, location, description]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            # Insert vehicle into Vehicle table
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
                return JsonResponse({'message': 'No cars found'}, status=404)

        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
