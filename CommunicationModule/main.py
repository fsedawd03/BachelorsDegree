from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from Controllers.EmailDataController import emailData_controller_router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging

app = FastAPI()

#@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	logging.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

# Include the routers from the controller module
app.include_router(emailData_controller_router, prefix="/v1.0/phishing")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)
