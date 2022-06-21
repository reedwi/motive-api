from fastapi import FastAPI

def create_app():
    description = '''
    Motive API Wrapper will get all Vehicles, Drivers, and from a single simple API Interface
    ## Vehicles
    Gets all vehicles in the account

    ## Drivers
    Gets all users in the account

    ## Assets
    Gets all assets in the account

    ## Install
    To install the app, navigate to /auth. There will be a URL in the response. Use this URL to install the app. This 
    then hits the Pipedream webhook to generate a token. Upon completion it will then send all Users, Vehicles, and Assets to the second
    pipedream workflow I have in the pipdream account currently.
    '''

    app = FastAPI(
        title="Motive API Wrapper",
        description=description,
        version='0.1'
    )

    return app