from ML_Model.createModel import MlModels
from DTO.EmailData import EmailData


class EmailDataService:
    def __init__(self):
        self.models = MlModels()

    def runModel(self, inputData: EmailData) -> int:
        return self.models.LogReg(inputData)
    def testModel(self, inputData: EmailData) -> int:
        return self.models.RandForest(inputData)
