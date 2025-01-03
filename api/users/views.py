# users/views.py
from psycopg2.extras import RealDictCursor
import bcrypt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .db_utils import get_connection
import json

import psycopg2  # Import psycopg2 for database interaction
from psycopg2 import Binary  # Import Binary for handling binary data
from django.http import StreamingHttpResponse
import time
import threading
from queue import Queue

# Global dictionary to store message queues for each chat
chat_queues = {}

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
            # Get vehicle_data from the form data (not JSON)
            vehicle_data = json.loads(request.POST.get('vehicle_data'))  # vehicle_data should be passed as a string
            print(f"Received Data: {vehicle_data}")

            # Extracting the values from the parsed data
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

            # Validate required fields
            if not all([brand, model_name, year, mileage, motor_power, price, location, description, vehicle_type]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # Proceed with inserting the data into the database
            # Insert into Vehicle table
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

                    # Insert additional vehicle data depending on vehicle type
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

                    # Insert ad into Ad table
                    cursor.execute("""
                        INSERT INTO Ad (user_id, vehicle_id, price, location, description)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING ad_id;
                    """, (user_id, vehicle_id, price, location, description))
                    ad_id = cursor.fetchone()[0]

                    # Check if any files are uploaded
                    images = request.FILES.getlist('images')
                    image_urls = []
                    if images:
                        print(f"Found {len(images)} image(s).")  # Debugging log to check image files

                        for image in images:
                            # Read the image as binary data
                            image_data = image.read()
                            print(f"Image Size: {len(image_data)} bytes")  # Debugging log for image size

                            # Generate a unique name for each image to avoid conflicts
                            image_name = f"vehicle_{ad_id}_{image.name}"
                            image_path = default_storage.save(f'images/{image_name}', ContentFile(image_data))  # Save the image to storage
                            image_url = f"/media/{image_path}"  # URL path for the image

                            # Insert both the image data and the image URL into the Image table
                            cursor.execute("""
                                INSERT INTO Image (ad_id, image_data, image_url)
                                VALUES (%s, %s, %s);
                            """, (ad_id, Binary(image_data), image_url))  # Insert both binary data and the URL

                            # Collect the URLs to return
                            image_urls.append(image_url)

                     # Check if expert report PDF is uploaded
                    pdf_file = request.FILES.get('pdf_file')  # Expect a file input with the name 'pdf_file'
                    if pdf_file:
                        # Read the PDF file as binary data
                        pdf_data = pdf_file.read()

                        # Generate a unique file name for the PDF file
                        pdf_filename = f"expert_report_{ad_id}.pdf"
                        pdf_path = default_storage.save(f'expert_reports/{pdf_filename}', ContentFile(pdf_data))  # Save the file to storage
                        pdf_url = f"/media/{pdf_path}"  # URL path for the PDF
                        # Insert the expert report into the ExpertReport table
                        cursor.execute("""
                            INSERT INTO ExpertReport (ad_id, expert_name, pdf_data, pdf_url)
                            VALUES (%s, %s, %s, %s)
                            RETURNING report_id;
                        """, (ad_id, 'expert_name', Binary(pdf_data), pdf_url))
                        report_id = cursor.fetchone()[0]  # Get the inserted report_id

                    conn.commit()  # Commit transaction

            # Return the response with success message and image URLs
            return JsonResponse({'message': 'Vehicle ad created successfully', 'ad_id': ad_id, 'image_urls': image_urls, 'pdf_url': pdf_url}, status=201)

        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

@csrf_exempt
def get_all_cars(request):
    if request.method == 'GET':
        try:
            # Query the active_listings view to get car ads
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
                return JsonResponse({'cars': []}, status=200)  # Return empty array if no cars

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

            # Fetch user data along with user type from the database
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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .db_utils import get_connection
from psycopg2.extras import RealDictCursor
@csrf_exempt
def get_car_details(request, ad_id):
    if request.method == 'GET':
        try:
            # Fetch car details from the active_listings view
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
                return JsonResponse(car, status=200)  # Return the car details including image_urls
            else:
                return JsonResponse({'error': 'Car not found or unavailable'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def make_offer(request):
    if request.method == 'POST':
        try:
            # Parse request data
            data = json.loads(request.body)
            ad_id = data.get('ad_id')
            offered_price = data.get('offered_price')
            user_id = data.get('user_id')

            # Validate required fields
            if not all([ad_id, offered_price, user_id]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # Validate offered_price
            if offered_price <= 0:
                return JsonResponse({'error': 'Offered price must be greater than 0'}, status=400)

            # Insert offer into PriceOffer table
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO PriceOffer (user_id, ad_id, offered_price)
                        VALUES (%s, %s, %s)
                        RETURNING offer_id;
                    """, (user_id, ad_id, offered_price))

                    offer_id = cursor.fetchone()[0]

                    # Commit the transaction
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
            # Retrieve seller_id from query parameters
            seller_id = request.GET.get('seller_id')  # seller_id is passed as a query parameter

            # Check if seller_id is provided
            if not seller_id:
                return JsonResponse({'error': 'seller_id is required'}, status=400)

            # Query the incoming_offers view for all offers associated with this seller
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
                return JsonResponse({'offers': []}, status=200)  # No offers found

        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

@csrf_exempt
def get_or_create_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            car_id = data.get('carId')
            buyer_id = data.get('currentUserId')
            seller_id = data.get('sellerId')

            with get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    # Check if chat exists
                    cursor.execute("""
                        SELECT chat_id FROM Chat
                        WHERE car_id = %s AND buyer_id = %s AND seller_id = %s
                    """, (car_id, buyer_id, seller_id))
                    chat = cursor.fetchone()

                    if not chat:
                        # Create new chat
                        cursor.execute("""
                            INSERT INTO Chat (car_id, buyer_id, seller_id)
                            VALUES (%s, %s, %s)
                            RETURNING chat_id
                        """, (car_id, buyer_id, seller_id))
                        chat = cursor.fetchone()

                    return JsonResponse({'chat_id': chat['chat_id']}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def get_chat_messages(request, car_id):
    if request.method == 'GET':
        try:
            user_id = request.GET.get('userId')
            
            with get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT 
                            message_id as id,
                            content,
                            sender_id as "senderId",
                            sender_name as "senderName",
                            timestamp
                        FROM chat_messages
                        WHERE car_id = %s
                        ORDER BY timestamp ASC
                    """, (car_id,))
                    messages = cursor.fetchall()

                    return JsonResponse(messages, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            car_id = data['carId']
            content = data['content']
            sender_id = data['senderId']
            
            with get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    # Get chat_id
                    cursor.execute("""
                        SELECT chat_id FROM Chat WHERE car_id = %s
                    """, (car_id,))
                    chat = cursor.fetchone()
                    
                    if not chat:
                        return JsonResponse({'error': 'Chat not found'}, status=404)

                    # Insert message
                    cursor.execute("""
                        INSERT INTO Message (chat_id, sender_id, content)
                        VALUES (%s, %s, %s)
                        RETURNING message_id, timestamp
                    """, (chat['chat_id'], sender_id, content))
                    new_message = cursor.fetchone()

                    # Notify connected clients
                    if car_id in chat_queues:
                        chat_queues[car_id].put(new_message)

                    return JsonResponse({'message': 'Message sent successfully'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def chat_stream(request, car_id):
    def event_stream():
        if car_id not in chat_queues:
            chat_queues[car_id] = Queue()

        while True:
            try:
                message = chat_queues[car_id].get(timeout=20)  # 20-second timeout
                yield f"data: {json.dumps(message)}\n\n"
            except:
                yield "data: {}\n\n"  # Keep-alive packet
            time.sleep(0.1)

    return StreamingHttpResponse(
        event_stream(),
        content_type='text/event-stream'
    )

