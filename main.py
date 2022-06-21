from pprint import pprint
from fastapi import FastAPI, Response, HTTPException, Request
from starlette.responses import RedirectResponse
from helpers.logger import get_logger
from api.motive import MotiveAPI
from models.motive_models import Vehicle, Driver, AcessToken, Asset
from helpers.data_helpers import parse_items
from app_initialization import create_app
from api.get_all import get_all_data
import json

app = create_app()

@app.get(
    '/vehicles', 
    responses={
        204: {
            "description": "No vehicles found",
            "content": []
        },
        400: {
            "description": "There was an error retrieving data"
        }
    },
    response_model=list[Vehicle], 
    status_code=200
)
async def vehicles(response: Response):
    try:
        api_module = MotiveAPI(item='vehicles')
        all_raw_vehicles = api_module.get_items()
        all_vehicles = parse_items(all_raw_vehicles, 'vehicle')
    except:
        raise HTTPException(status_code=400, detail='There was an error processing your request')

    if not all_vehicles:
        response.status_code = 204

    return all_vehicles

@app.get(
    '/drivers', 
    responses={
        204: {
            "description": "No drivers found",
            "content": []
        },
        400: {
            "description": "There was an error retrieving data"
        }
    },
    response_model=list[Driver],
    status_code=200
)
async def drivers(response: Response):
    try:
        api_module = MotiveAPI(item='users')
        all_raw_drivers = api_module.get_items()
        all_drivers = parse_items(all_raw_drivers, 'user')
    except:
        raise HTTPException(status_code=400, detail='There was an error processing your request')

    if not all_drivers:
        response.status_code = 204

    return all_drivers

@app.get(
    '/assets', 
    responses={
        204: {
            "description": "No assets found",
            "content": []
        },
        400: {
            "description": "There was an error retrieving data"
        }
    },
    response_model=list[Asset],
    status_code=200
)
async def assets(response: Response):
    try:
        api_module = MotiveAPI(item='assets')
        all_raw_drivers = api_module.get_items()
        all_assets = parse_items(all_raw_drivers, 'asset')
    except:
        raise HTTPException(status_code=400, detail='There was an error processing your request')

    if not all_assets:
        response.status_code = 204

    return all_assets

@app.get('/auth')
def auth():
    uri = MotiveAPI(request_type='install').auth()
    return {"message": f"Please install app at following link {uri}"}

@app.post('/token', status_code=200)
def receive_token(access_token: AcessToken):
    pprint(access_token)
    get_all_data(token=access_token.token)
    return {"Success": 200}

