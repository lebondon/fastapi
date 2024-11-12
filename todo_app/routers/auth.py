from fastapi import APIRouter       #allow us to rout from out main.py file to our auth.py file

router=APIRouter()

@router.get("/auth/")
async def get_user():
    return {'user':'authenticated'}

