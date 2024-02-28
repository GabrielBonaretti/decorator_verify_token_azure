import jwt
import requests
import json
from user import User
import datetime
from functools import wraps
from fastapi import Header, HTTPException


def verify_token_azure(function):
    """Decorator that verifies Azure Active Directory (AAD) tokens.

    Args:
        function: The function to be decorated.

    Returns:
        A decorator that wraps the original function and performs token verification.
    """

    @wraps(function)
    def wrapper(token: str = Header(...), *args, **kwargs):
        try:
            # Extract the token            
            try:
                # getting header information
                header = jwt.get_unverified_header(token)
                # getting body information
                body = jwt.decode(token, options={"verify_signature": False})
                
            except Exception as e:
                raise HTTPException(status_code=403, detail=f"Invalid token format or claims: {e}")
            
            # Create User object from token claims
            user = User(
                body.get("oid"),
                body.get("name"),
                body.get("preferred_username"), 
                body.get("roles")
            )
            
            tenant_id = "tenantID"  # Replace with your tenant ID
            app_id = "appID"  # Replace with your app ID
            discovery_url = f"https://login.microsoftonline.com/{tenant_id}/discovery/keys?appid={app_id}"

            try:
                response = requests.get(discovery_url)
                response.raise_for_status()

                result = json.loads(response.text)
                jwk_set = result.get("keys")

            except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
                raise HTTPException(status_code=403, detail=f"Error fetching or parsing JWKs: {e}")


            is_azure_token = False

            for jwk in jwk_set:
                if jwk.get("kid") == header.get("kid"):
                    is_azure_token = True
                    break  # Stop searching once a matching kid is found
            
            if not is_azure_token:
                raise HTTPException(status_code=403, detail=f"Invalid token: not an Azure AD token")
            
            # getting expiration data 
            timestamp_exp = body.get("exp")
            data_exp = datetime.datetime.fromtimestamp(timestamp_exp)

            if datetime.datetime.now() > data_exp:
                raise HTTPException(status_code=403, detail=f"The token is expired.")
            else:
                kwargs["user"] = user
                
                # Call the wrapped function with additional user information
                return function(*args, **kwargs)
        
        except IndexError:
            raise HTTPException(status_code=403, detail=f"Missing token argument")
        
            
    return wrapper           
