import psycopg2
from django.conf import settings

def get_connection():
    try:
        connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
