# Fast Strategy

A small FastAPI application that provides a race strategy based on temperature. The application takes a city and race length as inputs and returns the weather and suggested strategy. The results are stored in a Redis DB. The logic for how race strategy is modeled is explained in the notebook strategy-simulations.ipynb. 

A user can then retrieve the weather and strategy from the DB using the location route.

## Usage

### 1) Installation

#### Requirements:
- Docker
- API Key from [weatherstack](https://weatherstack.com). 

This method of running the application only requires Docker to be installed.

The App uses the weatherstack.com API. To use this application you will need an API Key. Weatherstack offers free subscriptions that you can sign up for.

Before building and running the docker container, you will need to set up your API key as an environment variable. 

This can be done in the CLI with the following commands. 

Ubuntu/Mac
```bash
export API_KEY=Your_API_KEY
```

Windows 
```bash
$env:API_KEY="Your_API_KEY"
```

Before proceeding make sure you do not have any other applications running on port 80 and 6379.
With the API_KEY set, navigate to the docker folder and run the following command.

```bash
docker compose build
```

Once the build is complete. You can then run the following command. 

```bash
docker compose up
```

This will spin up two containers. One is our application and the second will run the Redis DB. 

Navigate to [http://localhost/docs](http://localhost/docs) to open up the swagger page of the application. 


## Usage

### 1) Authentication

### 2) Recommendation Endpoint. 

Make a post request to the recommended endpoint. This will get the weather and recommend a race strategy. 

Example of Curl request made for a 40-lap race in Brussels. 

```bash
curl -X 'POST' \
  'http://localhost/recommend' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "laps": 40,
  "location": "Brussels"
}'
```
### 3) Location Endpoint. 

This endpoint will get the recommendation for that City from the Redis DB.

Example of Curl request getting strategy for Brussels from DB. 

```bash
curl -X 'GET' \
  'http://localhost/location/Brussels' \
  -H 'accept: application/json'
```

These requests can also be made using the Swagger UI. 



## License

[MIT](https://choosealicense.com/licenses/mit/)