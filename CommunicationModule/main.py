from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Controllers.EmailDataController import emailData_controller_router

app = FastAPI()

# Include the routers from the controller module
app.include_router(emailData_controller_router, prefix="/v1.0/phishing")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)
