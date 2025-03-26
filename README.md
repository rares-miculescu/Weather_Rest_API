# Weather REST API

## Introduction

REST API implemented using Docker Compose. The compose file includes 3 components:

- MongoDB database
- Mongo Express (database visualization tool)
- Flask API (request handler)

## API Endpoints

### Countries

- **POST /api/countries**
  * Add a country
  * **Body**: `{nume: String, lat: Double, lon: Double}`
  * **Success**: `201` with `{id: Int}`
  * **Errors**: `400` (wrong types / wrong number of arguments), `409` (duplicate country)
- **GET /api/countries**
  * Retrieve all countries
  * **Success**: `200` and list of countries
- **PUT /api/countries/:id**
  * Modify a country by ID
  * **Body**: `{id: Int, nume: String, lat: Double, lon: Double}`
  * **Success**: `200`
  * **Errors**: `400` (wrong types / wrong number of arguments / wrong arguments), `404` (country not found), `409` (duplicate country / wrong id / name already exists)
- **DELETE /api/countries/:id**
  * Delete a country by ID
  * **Success**: `200`
  * **Errors**: `404` (country not found)

### Cities (Requires existing country)

- **POST /api/cities**
  * Add a city
  * **Body**: `{idTara: Int, nume: String, lat: Double, lon: Double`
  * **Success**: `201` with `{id: Int}`
  * **Errors**: `400` (wrong types / wrong number of arguments / wrong arguments), `404` (country not found), `409` (duplicate country)
- **GET /api/cities**
  * Retrieve all cities
  * **Success**: `200` and list of cities
- **GET /api/cities/country/:id_tara**
  * Retrieve all cities from country_id={:id_Tara}
  * **Success**: `200` and list of cities
- **PUT /api/cities/:id**
  * Modify a city by ID
  * **Body**: `{id: Int, idTara: Int, nume: String, lat: Double, lon: Double}`
  * **Success**: `200`
  * **Errors**: `400` (wrong types / wrong number of arguments / wrong arguments), `404` (country not found / city not found), `409` (wrong id / name already exists)
- **DELETE /api/cities/:id**
  * Delete a country by ID
  * **Success**: `200`
  * **Errors**: `404` (city not found)

### Temperatures (Requires existing city)

- **POST /api/temperatures**
  * Add a temperature record
  * **Body**: `{id_oras: Int, valoare: Double}`
  * **Success**: `201` with `{id: Int}`
  * **Errors**: `400` (wrong types / wrong number of arguments / wrong arguments), `404` (city not found), `409` (temperature already exists)
- **GET /api/temperatures?lat=Double&lon=Double&from=Date&until=Date**
  * Filter temperatures by coordinates and/or time range
  * **Query Parameters**:
    - `lat`: Latitude (optional)
    - `lon`: Longitude (optional)
    - `from`: Start date (optional)
    - `until`: End date (optional)
  * **Notes**:
    - Returns all temperatures if no parameters provided.
    - Partial filters allowed (e.g., only `lat` or `from`).
  * **Success**: `200` and list of temperatures for given filters
- **GET /api/temperatures/cities/:id_oras?from=Date&until=Date**
  * Get temperatures for a specific city in given period (optional)
  * **Notes**:
    - Returns all temperatures for the city if no parameters provided.
  * **Success**: `200` and list of temperatures for city={id_oras} in given time period
  * **Error**: `404` (city not found)
- **GET /api/temperatures/countries/:id_tara?from=Date&until=Date**
  * Get temperatures for a specific country in given period (optional)
  * **Notes**:
    - Returns all temperatures for the country if no parameters provided.
  * **Success**: `200` and list of temperatures for country={id_tara} in given time period
  * **Error**: `404` (country not found)
- **PUT /api/temperatures/:id**
  * Update a temperature record for temperature_id={id}
  * **Body**: `{id: Int, idOras: Int, valoare: Double}`
  * **Success**: `200`
  * **Errors**: `400` (wrong types / wrong number of arguments / wrong arguments), `404` (temperature not found / city not found), `409` (wrong id)
- **DELETE /api/temperatures/:id**
  * Delete a temperature record by ID
  * **Success**: `200`
  * **Errors**: `404` (temperature not found)
