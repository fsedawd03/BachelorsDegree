from DTO.EmailData import EmailData
from Parsers.EmailParser import emailParser
import joblib
import os

def ML(inputData: EmailData) -> int:
    emailData = emailParser(inputData)
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'LogisticRegression.pkl')
    model = joblib.load(filename)
    prediction = model.predict(emailData)
    return int(prediction[0])
