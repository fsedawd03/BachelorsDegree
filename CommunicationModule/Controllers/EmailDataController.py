from fastapi import HTTPException
from DTO.EmailData import EmailData
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from Services.EmailDataService import EmailDataService

emailData_controller_router = InferringRouter()


@cbv(emailData_controller_router)
class EmailDataController:
    def __init__(self):
        self.emailDataService = EmailDataService()

    @emailData_controller_router.post('/runModel')
    def runModel(self, emailData: EmailData):
        try:
            return self.emailDataService.runModel(emailData)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @emailData_controller_router.post('/testModel')
    def testModel(self, emailData: EmailData):
        #try:
            return self.emailDataService.testModel(emailData)
       #except Exception as e:
            #raise HTTPException(status_code=500, detail=str(e))
