from fastapi import HTTPException, status

def bad_request(detail: str):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail=detail
    )

def unauthorised(detail: str = "Could not validate credentials"):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=detail, 
        headers={"WWW-Authenticate": "Bearer"}
    )

def forbidden(detail: str = "Permission denied"):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, 
        detail=detail
    )

def not_found(detail: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=detail
    )