# Fast Strategy

A small FastAPI application that provides a race strategy based on temperature. The application takes a city and race length as inputs and returns the weather and suggested strategy. The results are stored in a Redis DB. The logic for how race strategy is modeled is explained in the notebook strategy-simulations.ipynb. 

A user can then retrieve the weather and strategy from the DB using the location route.

## Usage

### 1) Docker (Recommended)

#### Requirements:
- Docker
- API Key from [weatherstack](https://weatherstack.com). 

This method of running the application only requires Docker to be installed.

The App uses the weatherstack API to get weather data. You can get a key at [weatherstack](https://weatherstack.com).

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

### 2) Run Locally

#### Requirements:
- Python 3.7 +
- API Key from [weatherstack](https://weatherstack.com).
- [Redis](https://redis.io/docs/getting-started/installation/)
- [Redis Json Module](https://redis.io/docs/stack/json/)


Get redis running locally. You can follow the [Redis Getting Started](https://redis.io/docs/getting-started/) page for detailed instructions on how to do this. 


With Redis installed ensure that you have the Redis Json Module installed [info](https://redis.io/docs/stack/json/).


To run the FastAPI application you will need to install the necessary modules. This can be done by running the following in the root directory 

```bash
pip install -r requirements.txt
```

You can then navigate to the app folder and run the following command. 

```bash
uvicorn main:app --reload
```

Lastly you need to set the weather API_KEY, you can follow the same steps provided above. 
Navigate to [http://localhost/docs](http://localhost/docs) to open up the swagger page of the application.  

## Usage

### 1) Authentication

The recommendation and location endpoints will require an access token. First, you will need to register to use the application. Users will be stored in the Redis DB.

Enter a username and password in the register endpoint. Once registered, you can use the "authorize" button on the swagger page to authenticate. The endpoints explained below should then work. You can also use the "authorize" button to logout. 

The token endpoint will return a valid token if given a valid username and password. This token will need to be added to the header of requests made to the application. If you authenticated using the "authorize" button on the swagger page then the token will be added to the headers for you and you can simply make requests from that point. 


Note: The security implemented in this application is purely for demonstration purposes and is not fit for a production-level application. 


### 2) Recommendation Endpoint. 

Make a post request to the /recommend endpoint. This will get the weather and recommend a race strategy. If you are using the swagger you can simply enter the number of laps and city.

Example of Curl request made for a 40-lap race in Brussels. 

```bash
curl -X 'POST' \
  'http://localhost/recommend/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer {Enter Token Here}' \
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
  -H 'accept: application/json' \
  -H 'Authorization: Bearer {Enter Token Here}'
```
