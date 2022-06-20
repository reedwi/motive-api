from fastapi import FastAPI

def create_app():
    description = '''
    Motive API Wrapper will get all Vehicles, Drivers, and from a single simple API Interface
    ## Vehicles
    Gets all vehicles in the account

    ## Drivers
    Gets all drivers in the account
    '''

    app = FastAPI(
        title="Motive API Wrapper",
        description=description,
        version='0.1'
    )

    return app