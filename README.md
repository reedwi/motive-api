# Motive API Wrapper
Small Python application that allows user to get all vehicles, drivers, and assets from the [Motive API](https://developer.gomotive.com/reference/introduction) within their account

## Considerations
Because of how the Motive developer app is setup and the losing of context between my app and pipedream, the app is broken into two general pieces, Install and Ongoing. 
### Install
In the install flow, you can navigate to /auth, where you will be prompted to install the app. On confirmation of install, the pipedream endpoint is hit and then pipedream is used to generate an access token. This access token is then passed back to my app at the /token endpoint and then triggers the app to get all Vehicles, Users and Assets from motive. As the data becomes available, it is then sent to a specified url that is currently instantiated in an environment variable and I have it as a second endpoint in pipedream currently. Upon successful completion, the app will then be installed and all data will have been sent to the end user. Because of the lack of context between my app, pipedream and motive, I made the decision to break this down. The context issue comes into play because without building some sort of user login on my app, looking into how headers and params work within the developer app, doing something with cookies etc, I am not able to tell who is actually installing the app. Anybody can navigate to the app and then it is passed to motive, then to pipedream, then back to the app. I cannot accurately keep track of the the install. My potential "easy" workaround was seeing that the "Client IP" is tracked within pipedream. So I was thinking I could use that has a PK in a table and then keep track of the refresh token, access token and IP together to then have this persist. In a real solution, this would be taken care of by true user provisioning within our app.

### Ongoing
There is then the ongoing portion of this app. This references a hardcoded refresh token in an env variable to simulate the same user using the app. I built out /vehicles, /drivers, and /users endpoints that when hit, will return all data for the specified object type in Motive. This then gives the end user the flexibility to get all data whenever they want. In a real context, this could be used by a fleet that is using 4 separate APIs and would hit and conglomerate all the object types from each of the APIs into a cleaned up singular response to the user.


## Design
This API is built using [FastAPI](https://fastapi.tiangolo.com) and leveraging some of the built-in data validation that is included within the framework. This validation is done thtough pydantic and also allows for the easy creration of API documentation.
``` mermaid
sequenceDiagram
    Requester->>API: Send get request to API
    API->>Motive: Retrieve all values from specified endpoint
    Motive->>API: Send all values back to API
    API->>API: Prepare and parse data
    API->>Requester: Send requested data to the requester
```

## API Docs
API docs can be referenced by navigating to "/docs" or "/redoc"

## Modules
### api
Contains functions to get data from motive api and also the models for the api responses
### helpers
Contains functions to clean and parse data as necessary
### tests
COntains test functions
### assets
Contains all static files and reference materials