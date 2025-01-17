# DbProjectRevisedVer

# For windows
1. Download docker desktop.
2. Open it.
3. Open admin terminal. 
4. Navigate to 
```bash
    cd path/to/dbBAckendRevised
```
5. Start tocker container
```bash
    docker-compose up
```
Wait until it finishes building up
6. Create a virtual env. in the dbBAckendRevised
```bash
    python -m venv venv
```
7. Activate the venv
```bash
    .\.venv\Scripts\Activate.ps1  
```
8. Navigate to 
```bash
    cd dbBackendRevised/api
```
9. Download Dependencies
```bash
    pip install -r requirements.txt
```
10. Run
```
    python manage.py runserver
```

# For Mac (generated by chatgpt)
For Mac:
1. Download Docker Desktop
2. Open Docker Desktop

3. Open Terminal from your applications or press Cmd + Space and type "Terminal".
4. Navigate to your project directory
```bash
    cd path/to/dbBackendRevised
```
5. Start Docker container
```bash
    docker-compose up
```
Wait for the container to finish building.
6. Create a virtual environment in the dbBackendRevised directory
```bash
    python3 -m venv venv
```
7. Activate the virtual environment
```bash
    source venv/bin/activate
```

8. Navigate to the API folder
```bash
    cd dbBackendRevised/api
```
9. Download dependencies
```bash
    pip install -r requirements.txt
```
10. Run the server:
```bash
    python manage.py runserver
```

- Maryam Reminders -
activate venv: 
.\.venv\Scripts\Activate.ps1  

folder: cd 
'C:\Users\Maryam Azimli\Documents\GitHub\CS353'

check db: 
docker exec -it postgres psql -U youruser -d yourdatabase

to list: \l or \du 

dummy create vehicle ad:
{
  "brand": "Toyota",
  "model_name": "Corolla",
  "year": 2020,
  "mileage": 15000,
  "motor_power": 130.5,
  "fuel_type": "Petrol",
  "fuel_tank_capacity": 50.0,
  "transmission_type": "Automatic",
  "body_type": "Sedan",
  "color": "Red",
  "price": 20000,
  "location": "New York",
  "description": "A well-maintained Toyota Corolla with low mileage.",
  "user_id": 1
}

motorcycle:
{
  "vehicle_type": "motorcycle",
  "brand": "Yamaha",
  "model_name": "YZF-R1",
  "year": 2020,
  "mileage": 1500,
  "fuel_type": "Petrol",
  "fuel_tank_capacity": 17,
  "motor_power": 200,
  "transmission_type": "Manual",
  "body_type": "Sport",
  "color": "Blue",
  "location": "New York, NY",
  "price": 12000,
  "description": "A high-performance sport motorcycle with advanced technology and exceptional handling.",
  "user_id": 1,  // Assuming user_id 1 is a Seller
  "wheelNumber": 2,
  "cylinderVolume": 998.5,
  "hasBasket": false
}