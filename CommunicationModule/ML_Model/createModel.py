from DTO.EmailData import EmailData
from Parsers.EmailParser import emailParser
from Parsers.EmailParserRand import emailParser as RForestParser
import joblib
import os


class MlModels():
    def LogReg(self,inputData: EmailData) -> int:
        emailData = emailParser(inputData)
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'LogisticRegression.pkl')
        model = joblib.load(filename)
        prediction = model.predict(emailData)
        return int(prediction[0])

    def RandForest(self,inputData: EmailData) -> int:
        emailData = RForestParser(inputData)
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'RandomForestClassifier.pkl')
        model = joblib.load(filename)
        prediction = model.predict(emailData)
        return int(prediction[0])
