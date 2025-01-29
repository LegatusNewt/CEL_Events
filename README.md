# CEL Events

This repository contains the code and resources for the Community Energy Labs take home coding challenge

## Run with Docker compose

To run the CEL Events project with Docker Compose
1. Clone the repository 
```
git clone git@github.com:LegatusNewt/CEL_Events.git
```
2. Navigate to the server directory, the Vue.js app is pre-built and served from the static files /dist directory on the flask server
3. If you don't have Docker already, [Install Docker](https://docs.docker.com/get-docker/), [Install Docker-Compose](https://docs.docker.com/compose/install/)
4. Run docker-compose up
5. Navigate to localhost:5000 in your browser

- Caveats!
You should see the docker build process happen and eventually the Flask App will be running on localhost:5000. If localhost:5000 is not available this won't work so you may need to change the ports in the docker-compose file and dockerr file, as well as the server-url in the Vue app and rebuild it with Vite

## Optional!! Building and Running Locally
You will need the following
- Python 3.12
- Poetry package manager ( no requirements.txt for pip here )
- npm or yarn , i prefer yarn

### Steps
1. Navigate to the client directory and install the dependencies with yarn
2. Run the command `yarn run vite build`
3. The vite.config is setup to build the Vue.js app into the server /dist folder
```
  build: {
    outDir: path.join('../../server', 'dist')
  }
```
4. Navigate to the server directory
5. Install packages with poetry `poetry install` , you may want to use the venv functionality of poetry
6. Set FLASK_APP Env variable 
```
export FLASK_APP="./communityenergylabsserver/flaskr/__init__.py"
```
7. Run Flask Server `poetry run flask run`


## Tech Stack
- Vue.js
- Vite Build tools
- Vue Pinia (state management)
- Quasar Component Library for Vue
- Python Flask
- Marshmallow (object schemas / serialization)

## Tests
There are some tests wrriten with pytest for the server using pytest however for the sake of time I only tested the basic routes and some basic functionality

## Repeating Events
I did not get to including a way to set events to repeat on the front end. There is a checkbox but it just sets a boolean. The repeating feature works with the seeded data you can see on the /schedule endpoint. Which you should see in the Calendar app.

If you post new event objects with the API you can include a repeat type in the body see this example from the seed data
```
{   
    "id" : 4,
    "name": "Test Event 4", 
    "start_time": "2025-01-04T00:00:00", 
    "end_time": "2025-01-04T06:00:00", 
    "repeats": True, 
    "repeat_types": [
        { 
            "type": RepeatTypes.DAY_OF_WEEK.value, 
            "num": 3
        }, 
        {
            "type": RepeatTypes.DAY_OF_WEEK.value,
            "num": 4 
        }
    ]
}
```
The /schedule endpoint runs some business logic to create repeated events in the return body based on the "RepeatType" and the modifer "num". In this "DAY_OF_WEEK" example the num represents the day of the week that is repeated. So this repeats the event every following Thursday and Friday (Monday = 0).