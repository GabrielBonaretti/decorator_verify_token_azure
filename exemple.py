from fastapi import Header

from verify_token_azure import verify_token_azure

@router.get("", response_model=List[ObjectResponseSchema])
@verify_token_azure # The decorator needs to come here
def get_all(db: Session = Depends(get_db), token: str = Header(...), user = None):
    """
    This is an example of an endpoint in fast api
    
    THe arguments you need to have when you use this decorator are:
        token: To get the JWT token in the request header, you need to pass the token as the key and the id as the value, for example:
        key      value   
        "token": "{your token jwt}"

        
        user: User returns the object of the user who is logged in, as well as their id, email, name and application functions. 
        An observation is that nothing is passed in the request to the user, it returns the value alone.
    """
    print(user)
    types = db.query(Object).all()
    return types