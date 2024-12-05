# Property Management System

A Django-based property management system with PostgreSQL and PostGIS integration for handling geospatial data. The system allows property owners to manage their properties through a Django Admin interface.

## Features

### Core Features
1. **Locations**:
   - Locations with hierarchical nesting (country, state, city).
   - Geospatial data integration using PostGIS (e.g., latitude, longitude).
   - Add locations via CSV import through the admin interface.

2. **Accommodations**:
   - Manage property details such as title, location, amenities, and pricing.
   - Store geolocation data to accommodations using PostGIS.
   - Support for multiple images and JSONB-based amenities storage.

3. **Localized Accommodation Details**:
   - Provide localized accommodation descriptions and policies

4. **Property Owner Management**:
   - Property owners can manage their own properties (after admin approval)
   - Property owners can sign up and await approval before publishing their properties

5. **Geospatial Support**:
   - Advanced location-based data handling with PostGIS.

6. **Sitemap Generation**:
   - Automaticlly generate a sitemap.json file for all country locations alphabetically by location name.

7. **Partition**
   - Partition the database for optimize the application
 

## Project Structure

```plaintext
Inventory_Management/                          # Main project directory
│
├── sitemap.json                               # Sitemap configuration or generated file 
├── Inventory_Management/                      # Project settings and configuration files
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── property_management/                      # Main Django app for managing properties
│   ├── __init__.py
│   ├── admin.py                               # Django admin interface configuration
│   ├── apps.py                                # App-specific configuration
│   ├── forms.py                               # Forms for property management
│   ├── models.py                              # Data models for the app (e.g., properties, owners)
│   ├── resources.py                           # External data handling or integration (e.g., CSV imports)
│   ├── tests.py                               # Unit tests for the app
│   ├── urls.py                                # URL routing for the app
│   ├── views.py                               # Views for rendering responses
│   ├── migrations/                           # Database migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_remove_accommodation_images_and_more.py
│   │   ├── 0003_accommodation_images.py
        ├── 0004_auto_partition_accommodation.py
│   │   └── __init__.py
│   │
│   ├── management/                            # Custom management commands
│   │   ├── __init__.py
│   │   ├── commands/
│   │   │   ├── create_property_owners_group.py  # Command to create property owner groups
│   │   │   ├── generate_sitemap.py           # Command to generate sitemap
│   │   │   └── populate_location_data.py     # Command to populate location data
│   │
│   └── templates/                             # HTML templates for rendering pages
│       ├── base_generic.html                  # Base template
│       ├── property_owner_sign_up.html        # Template for property owner sign-up
│       ├── property_owner_sign_up_success.html # Template for successful sign-up
│       └── __init__.py
│
├── .coveragerc                                # Coverage configuration file for tests
├── Dockerfile                                 # Docker configuration for containerizing the app
├── docker-compose.yml                        # Docker Compose file to manage multiple services
├── manage.py                                  # Django command-line utility
├── requirements.txt                          # Dependencies for the Docker Project
help.txt                                      # Helpful information or documentation 
.gitignore                                     # Git ignore file 
requirements.txt                              # Dependencies for the Project
```



## Project Setup

### Prerequisites
- **Python 3.8+**
- **PostgreSQL** with **PostGIS extensions**
- **Docker** and **Docker Compose**

### Docker Configuration
This project uses Docker and Docker Compose to run the application with all necessary services, including the PostgreSQL database with the PostGIS extension.

- The `Dockerfile` sets up the application container.
- The `docker-compose.yml` file defines the services required to run the application (Django, PostgreSQL, etc.).

### Installation Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
 
4. Configure the database in settings.py:
    ```plaintext
    Update DATABASES with your PostgreSQL credentials and enable PostGIS.
    ```
 
### Running the Application
 
1. Docker Set Up:
   ```bash
   docker-compose up --build -d
   ```
   
2. Apply migrations:
   ```bash
   docker exec -it django_app python manage.py makemigrations
   docker exec -it django_app python manage.py migrate
   ```

3. Create a superuser:
   ```bash
   docker exec -it django_app python manage.py createsuperuser
   ```

4. Start the server:
   ```bash
   docker exec -it django_app python manage.py runserver
   ```
   
5. Access the application at http://localhost:8000/

## Usage

1. `http://localhost:8000`

2. `http://localhost:8000/sign-up/` for Property Owner signup

3. Access the admin panel at `http://localhost:8000/admin/` and log in with your superuser credentials.

## Command-Line Utility

- **Populate initial location data:**
    To populate initial location data, run:
   ```bash
   docker exec -it django_app python manage.py populate_location_data
   ```
   
- **Generate sitemap:**
    To generate the sitemap, open the bash shell:
   ```bash
   docker exec -it django_app bash
   ```
   Then run:
   ```bash
   python manage.py generate_sitemap
   ```
   
- **Update the Property Owners Group:**
    Run the following command to create or update the property owners group:
   ```bash
   docker exec -it django_app python manage.py create_property_owners_group
   ```

## Add accommodation Amenities field

    ```
    [
     "Free Wi-Fi",
     "Air Conditioning",
     "Swimming Pool",
     "Pet-Friendly",
     "Room Service",
     "Gym Access"
    ]
    ```

## Add Localized Accommodation Aolicy field

- language: en

    ``` 
    {
    "pet_policy" : "Pets are not allowed.",
    "smoking_policy" : "Smoking is prohibited indoors."
    }
    ```
- language: Len

    ``` 
    {
    "pet_policy" : "No se permiten mascotas.",
    "smoking_policy" : "Está prohibido fumar en el interior."
    }
    ```

## CSV Format for Locations

**To import locations via CSV, ensure that the CSV file follows this format:**

   ```bash
   id,title,center,parent,location_type,country_code,state_abbr,city,created_at,updated_at
   BD,Bangladesh,"POINT(90.3563 23.685)",,country,BD,,,,
   BD-CTG,Chittagong,"POINT(91.815536 22.341900)",BD,state,BD,CTG,,,
   BD-CTG-KH,Khulshi,"POINT(91.815536 22.341900)",BD-CTG,city,BD,CTG,"Khulshi",,
   BD-DHA,Dhaka,"POINT(90.4125 23.8103)",BD,state,BD,DHA,,,
   BD-DHA-MI,Mirpur,"POINT(90.4125 23.8103)",BD-DHA,city,BD,DHA,"Mirpur",,
   ```

## Testing
To run unit tests for the project, use:

   ```bash
   docker exec -it django_app python manage.py test
   ```

To see the coverage report, run:

   ```bash
   docker exec -it django_app coverage report
   ```
   
## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Contributing

Feel free to fork the repository and submit pull requests. Please follow the standard GitHub workflow and ensure that any contributions are well-tested.