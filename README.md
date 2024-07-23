# Berlin District Data Management API

This Flask application provides a REST API for managing and querying data related to Berlin's districts, urban planning areas, and bicycle theft incidents.

## Features

- CRUD operations for district boundaries, planning areas, and bicycle theft data
- Cross-origin resource sharing (CORS) support
- PostgreSQL database integration
- RESTful API endpoints for data retrieval and manipulation

## Prerequisites

- Python 3.x
- PostgreSQL
- Flask
- Flask-SQLAlchemy
- Flask-CORS

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your PostgreSQL database and update the `SQLALCHEMY_DATABASE_URI` in the code with your database credentials.

## Database Structure

The application uses three main tables:

1. `bezirksgrenzen`: Stores information about district boundaries
2. `lor_planungs_raeume_2021`: Stores information about urban planning areas (LOR)
3. `fahrraddiebstahl`: Stores information about bicycle thefts

## API Endpoints

### District Boundaries (Bezirksgrenzen)

- GET `/bezirksgrenzens`: Retrieve all district boundary entries
- GET `/bezirksgrenzen/<bez_id>`: Retrieve a specific district boundary entry
- POST `/bezirksgrenzen`: Create a new district boundary entry
- PUT `/bezirksgrenzen/<id>`: Update a district boundary entry
- DELETE `/bezirksgrenzen/<gml_id>`: Delete a district boundary entry

### Planning Areas (LOR)

- GET `/lorPlanungsRaeume2021s`: Retrieve all planning area entries
- GET `/lorPlanungsRaeume2021/<lor_id>`: Retrieve a specific planning area entry
- DELETE `/lorPlanungsRaeume2021/<plr_id>`: Delete a planning area entry

### Bicycle Thefts (Fahrraddiebstahl)

- GET `/fahrraddiebstahls`: Retrieve all bicycle theft entries
- GET `/fahrraddiebstahl/<fahr_id>`: Retrieve a specific bicycle theft entry
- DELETE `/fahrraddiebstahl/<fahrraddiebstahl_id>`: Delete a bicycle theft entry

### Join Operations

- GET `/gemeinde_name_from_lor/<lor_id>`: Retrieve joined data from district boundaries and planning areas
- GET `/plr_name_from_fahr/<fahr_id>`: Retrieve joined data from planning areas and bicycle thefts

## Running the Application

To run the application, execute:

```
python app.py
```

The server will start, and you can access the API at `http://localhost:5000`.

## Notes

- The application uses SQLAlchemy ORM for database operations.
- CORS is enabled for all origins with credential support.
- Ensure that your PostgreSQL server is running and accessible before starting the application.


## License

This project is licensed under the [MIT License](LICENSE).
