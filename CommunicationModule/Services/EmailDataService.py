from ML_Model.createModel import ML
from DTO.EmailData import EmailData


class EmailDataService:
    def __init__(self):
        self.model = ML

    def runModel(self, inputData: EmailData) -> int:
        return self.model(inputData)
