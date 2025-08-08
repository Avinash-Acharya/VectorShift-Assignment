# hubspot.py

import json
import secrets
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
import httpx
import asyncio
import base64
import requests
from integrations.integration_item import IntegrationItem
from config import config
from urllib.parse import urlencode

from redis_client import add_key_value_redis, get_value_redis, delete_key_redis

# Validate and get HubSpot credentials from environment variables
config.validate_hubspot_credentials()
CLIENT_ID = config.HUBSPOT_CLIENT_ID
CLIENT_SECRET = config.HUBSPOT_CLIENT_SECRET

REDIRECT_URI = 'http://localhost:8000/integrations/hubspot/oauth2callback'
SCOPES = 'crm.objects.contacts.read crm.objects.companies.read crm.objects.deals.read'

async def authorize_hubspot(user_id, org_id):
    state_data = {
        'state': secrets.token_urlsafe(32),
        'user_id': user_id,
        'org_id': org_id
    }
    encoded_state = base64.urlsafe_b64encode(json.dumps(state_data).encode('utf-8')).decode('utf-8')
    # Build the authorization URL with proper URL encoding of query parameters
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': SCOPES,  # spaces will be encoded as %20 by urlencode
        'redirect_uri': REDIRECT_URI,
        'state': encoded_state,
    }
    auth_url = f"https://app.hubspot.com/oauth/authorize?{urlencode(params)}"
    await add_key_value_redis(f'hubspot_state:{org_id}:{user_id}', json.dumps(state_data), expire=600)
    
    return auth_url

async def oauth2callback_hubspot(request: Request):
    if request.query_params.get('error'):
        raise HTTPException(status_code=400, detail=request.query_params.get('error_description'))
    
    code = request.query_params.get('code')
    encoded_state = request.query_params.get('state')
    
    if not encoded_state:
        raise HTTPException(status_code=400, detail='Missing state parameter.')
    
    try:
        state_data = json.loads(base64.urlsafe_b64decode(encoded_state).decode('utf-8'))
    except:
        raise HTTPException(status_code=400, detail='Invalid state parameter.')
    
    original_state = state_data.get('state')
    user_id = state_data.get('user_id')
    org_id = state_data.get('org_id')
    
    saved_state = await get_value_redis(f'hubspot_state:{org_id}:{user_id}')
    
    if not saved_state or original_state != json.loads(saved_state).get('state'):
        raise HTTPException(status_code=400, detail='State does not match.')
    
    async with httpx.AsyncClient() as client:
        response, _ = await asyncio.gather(
            client.post(
                'https://api.hubapi.com/oauth/v1/token',
                data={
                    'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': REDIRECT_URI,
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                },
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
            ),
            delete_key_redis(f'hubspot_state:{org_id}:{user_id}'),
        )
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail='Failed to exchange code for token.')
    # Debug: print token payload (sanitized) before saving to Redis
    tokens = response.json()
    try:
        access_token = tokens.get('access_token')
        redacted = {
            'hub_id': tokens.get('hub_id'),  # may be absent in token response
            'expires_in': tokens.get('expires_in'),
            'scope': tokens.get('scope'),   # may be absent
            'token_type': tokens.get('token_type'),
            'access_token_preview': (access_token or '')[:8] + '...' if access_token else None,
            'refresh_token_present': bool(tokens.get('refresh_token')),
        }
        print(f"HubSpot OAuth token response (sanitized): {redacted}")
    except Exception as e:
        print(f"Failed to log HubSpot token response: {e}")

    # Optional: call HubSpot access token info endpoint to enrich with hub_id and scopes
    try:
        if tokens.get('access_token'):
            async with httpx.AsyncClient() as client_info:
                info_resp = await client_info.get(
                    f"https://api.hubapi.com/oauth/v1/access-tokens/{tokens['access_token']}"
                )
            if info_resp.status_code == 200:
                info = info_resp.json()
                # info typically contains: hub_id, user, scopes, token_type, etc.
                tokens['hub_id'] = tokens.get('hub_id') or info.get('hub_id')
                tokens['scopes'] = info.get('scopes')
                print(f"HubSpot token info: hub_id={tokens['hub_id']}, scopes={tokens.get('scopes')}")
            else:
                print(f"Failed to fetch token info: {info_resp.status_code} - {info_resp.text}")
    except Exception as e:
        print(f"Error during token info fetch: {e}")

    await add_key_value_redis(f'hubspot_credentials:{org_id}:{user_id}', json.dumps(tokens), expire=600)
    
    close_window_script = """
    <html>
        <script>
            window.close();
        </script>
    </html>
    """
    return HTMLResponse(content=close_window_script)

async def get_hubspot_credentials(user_id, org_id):
    credentials = await get_value_redis(f'hubspot_credentials:{org_id}:{user_id}')
    if not credentials:
        raise HTTPException(status_code=400, detail='No credentials found.')
    credentials = json.loads(credentials)
    await delete_key_redis(f'hubspot_credentials:{org_id}:{user_id}')
    
    return credentials

def create_integration_item_metadata_object(response_json: dict, item_type: str) -> IntegrationItem:
    """Creates an integration metadata object from the HubSpot API response"""
    
    # Extract common fields from HubSpot objects
    item_id = response_json.get('id', '')
    properties = response_json.get('properties', {})
    
    # Get name based on object type
    name = ''
    if item_type == 'contact':
        first_name = properties.get('firstname', '')
        last_name = properties.get('lastname', '')
        name = f"{first_name} {last_name}".strip() or properties.get('email', f'Contact {item_id}')
    elif item_type == 'company':
        name = properties.get('name', f'Company {item_id}')
    elif item_type == 'deal':
        name = properties.get('dealname', f'Deal {item_id}')
    else:
        name = f'{item_type.title()} {item_id}'
    
    # Get timestamps
    created_at = properties.get('createdate', '')
    updated_at = properties.get('lastmodifieddate', '')
    
    integration_item_metadata = IntegrationItem(
        id=f"{item_type}_{item_id}",
        name=name,
        type=item_type,
        creation_time=created_at,
        last_modified_time=updated_at,
        parent_id=None,
        parent_path_or_name=None,
    )
    
    return integration_item_metadata

async def get_items_hubspot(credentials) -> list[IntegrationItem]:
    """Fetches and returns HubSpot CRM objects as IntegrationItem objects"""
    credentials = json.loads(credentials)
    access_token = credentials.get('access_token')
    refresh_token = credentials.get('refresh_token')
    
    if not access_token:
        raise HTTPException(status_code=400, detail='Missing access token.')
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    list_of_integration_items = []
    
    # Define the objects to fetch and their endpoints
    objects_to_fetch = [
        ('contacts', 'https://api.hubapi.com/crm/v3/objects/contacts'),
        ('companies', 'https://api.hubapi.com/crm/v3/objects/companies'),
        ('deals', 'https://api.hubapi.com/crm/v3/objects/deals'),
    ]
    
    def try_refresh_and_update_headers() -> bool:
        """Attempt to refresh the access token using the provided refresh_token.
        Returns True if refreshed successfully and updates headers; else False.
        """
        nonlocal access_token, headers
        if not refresh_token:
            return False
        try:
            resp = requests.post(
                'https://api.hubapi.com/oauth/v1/token',
                data={
                    'grant_type': 'refresh_token',
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                    'redirect_uri': REDIRECT_URI,
                    'refresh_token': refresh_token,
                },
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            if resp.status_code == 200:
                refreshed = resp.json()
                access_token = refreshed.get('access_token') or access_token
                headers['Authorization'] = f'Bearer {access_token}'
                # Do not print full tokens
                print('HubSpot access token refreshed successfully')
                return True
            else:
                print(f"Failed to refresh token: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"Error during token refresh: {e}")
        return False

    for object_type, endpoint in objects_to_fetch:
        try:
            # Fetch first page of results
            params = {
                'limit': 100,
                'properties': 'firstname,lastname,email,name,dealname,createdate,lastmodifieddate'
            }
            
            response = requests.get(endpoint, headers=headers, params=params)
            
            if response.status_code == 401:
                # Try refreshing the token once and retry the request
                if try_refresh_and_update_headers():
                    response = requests.get(endpoint, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                print(f"HubSpot API fetched {len(results)} {object_type}")
                
                # Convert singular form for item type
                item_type = object_type[:-1] if object_type.endswith('s') else object_type
                
                for item in results:
                    integration_item = create_integration_item_metadata_object(item, item_type)
                    list_of_integration_items.append(integration_item)
                # Optional: log a small sample of raw items for verification
                try:
                    sample = results[:2]
                    if sample:
                        print(f"Sample {object_type} (first 2): {json.dumps(sample)[:500]}")
                except Exception as e:
                    print(f"Failed to print sample {object_type}: {e}")
                    
            else:
                print(f"Failed to fetch {object_type}: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"Error fetching {object_type}: {str(e)}")
    
    print(f'HubSpot integration items (count): {len(list_of_integration_items)}')
    # Ensure JSON-serializable response: convert IntegrationItem objects to plain dicts
    serializable_items = [vars(item) for item in list_of_integration_items]
    return serializable_items