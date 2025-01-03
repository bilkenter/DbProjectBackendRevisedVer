from psycopg2.extras import RealDictCursor
import bcrypt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .db_utils import get_connection
import json

import psycopg2 
from psycopg2 import Binary


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            email = data['email']
            user_type = data['userType']
            notificationPreference = data['notificationPreference']

            """if not username or not password or not email or not phone_number or not user_type or not notification_preferences:"""
            if not username or not password or not email or not user_type or not notificationPreference:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO UserAccount (username, pass, email)
                        VALUES (%s, %s, %s)
                        RETURNING user_id;
                    """, (username, hashed_password.decode('utf-8'), email)) 
                    new_user_id = cursor.fetchone()[0]

                    cursor.execute("""
                        INSERT INTO AppUser (user_id, notification_preference)
                        VALUES (%s, %s);
                    """, (new_user_id, notificationPreference))

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

            if not email or not password:
                return JsonResponse({'error': 'Missing username or password'}, status=400)

            with get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT user_id, username, email, pass
                        FROM UserAccount
                        WHERE email = %s;
                    """, (email,))
                    user = cursor.fetchone()

            if user:
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

from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from psycopg2 import Binary
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .db_utils import get_connection

@csrf_exempt
def create_vehicle_ad(request):
    if request.method == 'POST':
        try:
            vehicle_data = json.loads(request.POST.get('vehicle_data')) 
            print(f"Received Data: {vehicle_data}")

            brand = vehicle_data.get('brand')
            model_name = vehicle_data.get('model_name')
            year = vehicle_data.get('year')
            mileage = vehicle_data.get('mileage')
            motor_power = vehicle_data.get('motor_power')
            fuel_type = vehicle_data.get('fuel_type')
            fuel_tank_capacity = vehicle_data.get('fuel_tank_capacity')
            transmission_type = vehicle_data.get('transmission_type')
            body_type = vehicle_data.get('body_type')
            color = vehicle_data.get('color')
            price = vehicle_data.get('price')
            location = vehicle_data.get('location')
            description = vehicle_data.get('description')
            user_id = vehicle_data.get('user_id')
            vehicle_type = vehicle_data.get('vehicle_type')

            if not all([brand, model_name, year, mileage, motor_power, price, location, description, vehicle_type]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Vehicle (brand, model_name, year, mileage, motor_power, fuel_type, fuel_tank_capacity,
                                             transmission_type, body_type, color, vehicle_type)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING vehicle_id;
                    """, (brand, model_name, year, mileage, motor_power, fuel_type, fuel_tank_capacity, transmission_type,
                          body_type, color, vehicle_type))
                    vehicle_id = cursor.fetchone()[0]

                    if vehicle_type == "Car":
                        num_of_doors = vehicle_data.get('numOfDoors')
                        cursor.execute("""
                            INSERT INTO Car (vehicle_id, number_of_doors)
                            VALUES (%s, %s);
                        """, (vehicle_id, num_of_doors))
                        

                    elif vehicle_type == "Motorcycle":
                        wheel_number = vehicle_data.get('wheelNumber')
                        cylinder_volume = vehicle_data.get('cylinderVolume')
                        has_basket = vehicle_data.get('hasBasket', False)
                        cursor.execute("""
                            INSERT INTO Motorcycle (vehicle_id, wheel_number, cylinder_volume, has_basket)
                            VALUES (%s, %s, %s, %s);
                        """, (vehicle_id, wheel_number, cylinder_volume, has_basket))

                    elif vehicle_type == "Van":
                        seat_number = vehicle_data.get('seatNumber')
                        roof_height = vehicle_data.get('roofHeight')
                        cabin_space = vehicle_data.get('cabinSpace')
                        has_sliding_door = vehicle_data.get('hasSlidingDoor', False)
                        cursor.execute("""
                            INSERT INTO Van (vehicle_id, seat_number, roof_height, cabin_space, has_sliding_door)
                            VALUES (%s, %s, %s, %s, %s);
                        """, (vehicle_id, seat_number, roof_height, cabin_space, has_sliding_door))

                    cursor.execute("""
                        INSERT INTO Ad (user_id, vehicle_id, price, location, description)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING ad_id;
                    """, (user_id, vehicle_id, price, location, description))
                    ad_id = cursor.fetchone()[0]

                    images = request.FILES.getlist('images')
                    image_urls = []
                    if images:
                        print(f"Found {len(images)} image(s).")  

                        for image in images:
                            image_data = image.read()
                            print(f"Image Size: {len(image_data)} bytes") 

                            image_name = f"vehicle_{ad_id}_{image.name}"
                            image_path = default_storage.save(f'images/{image_name}', ContentFile(image_data))
                            image_url = f"/media/{image_path}"  

                            cursor.execute("""
                                INSERT INTO Image (ad_id, image_data, image_url)
                                VALUES (%s, %s, %s);
                            """, (ad_id, Binary(image_data), image_url)) 

                            image_urls.append(image_url)

                    pdf_file = request.FILES.get('pdf_file') 
                    if pdf_file:
                        pdf_data = pdf_file.read()

                        pdf_filename = f"expert_report_{ad_id}.pdf"
                        pdf_path = default_storage.save(f'expert_reports/{pdf_filename}', ContentFile(pdf_data))  
                        pdf_url = f"/media/{pdf_path}"
                        cursor.execute("""
                            INSERT INTO ExpertReport (ad_id, expert_name, pdf_data, pdf_url)
                            VALUES (%s, %s, %s, %s)
                            RETURNING report_id;
                        """, (ad_id, 'expert_name', Binary(pdf_data), pdf_url))
                        report_id = cursor.fetchone()[0] 

                    conn.commit()  

            return JsonResponse({'message': 'Vehicle ad created successfully', 'ad_id': ad_id, 'image_urls': image_urls, 'pdf_url': pdf_url}, status=201)

        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

@csrf_exempt
def get_all_cars(request):
    if request.method == 'GET':
        try:
            with get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT
                            ad_id,
                            seller_id,
                            brand,
                            model_name,
                            year,
                            price,
                            location,
                            mileage,
                            motor_power,
                            fuel_type,
                            transmission_type,
                            body_type,
                            color,
                            description,
                            image_urls,
                            posting_date
                        FROM active_listings
                    """)
                    cars = cursor.fetchall()

            if cars:
                return JsonResponse({'cars': cars}, status=200)
            else:
                return JsonResponse({'cars': []}, status=200)

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
            user_id = request.GET.get('user_id') 
            
            if not user_id:
                return JsonResponse({'error': 'User ID is required'}, status=400)

            with get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT u.username, u.email, u.user_id,
                               CASE
                                   WHEN s.user_id IS NOT NULL THEN 'Seller'
                                   WHEN b.user_id IS NOT NULL THEN 'Buyer'
                                   WHEN m.user_id IS NOT NULL THEN 'Moderator'
                                   WHEN admin.user_id IS NOT NULL THEN 'Admin'
                                   ELSE 'Unknown'
                               END AS user_type
                        FROM UserAccount u
                        LEFT JOIN Seller s ON u.user_id = s.user_id
                        LEFT JOIN Buyer b ON u.user_id = b.user_id
                        LEFT JOIN Moderator m ON u.user_id = m.user_id
                        LEFT JOIN AdminAccount admin ON u.user_id = admin.user_id
                        WHERE u.user_id = %s;
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
            user_id = request.GET.get('user_id') 
            print(f"Received Data: {user_id}")

            if not user_id:
                return JsonResponse({'error': 'User ID is required'}, status=400)

            with get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT * FROM seller_ads
                        WHERE seller_id = %s;
                    """, (user_id,))
                    ads = cursor.fetchall()
                    print(f"Received Data: {ads}")

            if ads:
                return JsonResponse({'ads': ads}, status=200)
            else:
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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .db_utils import get_connection
from psycopg2.extras import RealDictCursor
@csrf_exempt
def get_car_details(request, ad_id):
    if request.method == 'GET':
        try:
            with get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT
                            ad_id,
                            seller_id,
                            seller_name,
                            seller_email,
                            brand,
                            model_name,
                            year,
                            price,
                            location,
                            mileage,
                            motor_power,
                            fuel_type,
                            fuel_tank_capacity,
                            transmission_type,
                            body_type,
                            color,
                            description,
                            image_urls,
                            posting_date,
                            vehicle_type,
                            number_of_doors,
                            wheel_number,
                            cylinder_volume,
                            has_basket,
                            seat_number,
                            roof_height,
                            cabin_space,
                            has_sliding_door,
                            pdf
                        FROM active_listings
                        WHERE ad_id = %s;
                    """, (ad_id,))
                    car = cursor.fetchone()

            if car:
                return JsonResponse(car, status=200) 
            else:
                return JsonResponse({'error': 'Car not found or unavailable'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def make_offer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ad_id = data.get('ad_id')
            offered_price = data.get('offered_price')
            user_id = data.get('user_id')

            if not all([ad_id, offered_price, user_id]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            if offered_price <= 0:
                return JsonResponse({'error': 'Offered price must be greater than 0'}, status=400)

            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO PriceOffer (user_id, ad_id, offered_price)
                        VALUES (%s, %s, %s)
                        RETURNING offer_id;
                    """, (user_id, ad_id, offered_price))

                    offer_id = cursor.fetchone()[0]

                    conn.commit()

            return JsonResponse({'message': 'Offer made successfully', 'offer_id': offer_id}, status=201)

        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def get_incoming_offers(request):
    if request.method == 'GET':
        try:
            seller_id = request.GET.get('seller_id')  

            if not seller_id:
                return JsonResponse({'error': 'seller_id is required'}, status=400)

            with get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT
                            offer_id,
                            buyer_id,
                            buyer_username,
                            offered_price,
                            status,
                            offer_date,
                            ad_id,
                            seller_id,
                            brand,
                            model_name,
                            year
                        FROM incoming_offers
                        WHERE seller_id = %s;
                    """, (seller_id,))
                    offers = cursor.fetchall()

            if offers:
                return JsonResponse({'offers': offers}, status=200)
            else:
                return JsonResponse({'offers': []}, status=200) 

        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

@csrf_exempt
def get_buyer_offers(request):
    if request.method == 'GET':
        try:
            buyer_id = request.GET.get('buyer_id') 

            if not buyer_id:
                return JsonResponse({'error': 'buyer_id is required'}, status=400)

            with get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT
                            offer_id,
                            buyer_id,
                            buyer_username,
                            offered_price,
                            status,
                            offer_date,
                            ad_id,
                            seller_id,
                            brand,
                            model_name,
                            year
                        FROM incoming_offers
                        WHERE buyer_id = %s;
                    """, (buyer_id,))
                    offers = cursor.fetchall()

            if offers:
                return JsonResponse({'offers': offers}, status=200)
            else:
                return JsonResponse({'offers': []}, status=200) 

        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

@csrf_exempt
def accept_reject_offer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            offer_id = data.get('offer_id')
            action = data.get('action') 
            user_id = data.get('user_id') 

            if not all([offer_id, action, user_id]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            if action not in ['accepted', 'rejected']:
                return JsonResponse({'error': 'Invalid action, should be accepted or rejected'}, status=400)

            with get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT o.offer_id, o.user_id AS buyer_id, o.ad_id, o.offered_price, o.offer_status, o.offer_date,
                               a.vehicle_id, a.user_id AS seller_id
                        FROM PriceOffer o
                        JOIN Ad a ON o.ad_id = a.ad_id
                        WHERE o.offer_id = %s AND a.user_id = %s;  -- ensure the ad belongs to the seller
                    """, (offer_id, user_id))
                    offer = cursor.fetchone()

            if not offer:
                return JsonResponse({'error': 'Offer not found or you are not the seller for this ad'}, status=404)

            if action == 'accepted':
                with get_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("""
                            UPDATE PriceOffer
                            SET offer_status = 'rejected'
                            WHERE ad_id = %s AND offer_id != %s;
                        """, (offer['ad_id'], offer_id))

                        cursor.execute("""
                            UPDATE PriceOffer
                            SET offer_status = 'accepted'
                            WHERE offer_id = %s;
                        """, (offer_id,))

                        cursor.execute("""
                            INSERT INTO Transact (offer_id)
                            VALUES (%s)
                            RETURNING transaction_id;

                        """, (offer_id,))


                        transaction_id = cursor.fetchone()[0]

                        conn.commit()

                return JsonResponse({
                    'message': 'Offer accepted successfully',
                    'transaction_id': transaction_id
                }, status=200)

            elif action == 'rejected':
                with get_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("""
                            UPDATE PriceOffer
                            SET offer_status = 'rejected'
                            WHERE offer_id = %s;
                        """, (offer_id,))
                        conn.commit()

                return JsonResponse({'message': 'Offer rejected successfully'}, status=200)

        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
