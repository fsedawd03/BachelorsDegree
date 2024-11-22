import re
from email.parser import HeaderParser

import nltk
import pandas as pd
from bs4 import BeautifulSoup

from DTO.EmailData import EmailData


def containsWrapper(searchValue: str, text: str) -> int:
    return 1 if searchValue in text else 0

def remove_punct(text: str) -> str:
    txt = re.sub("[^a-zA-Z]", " ", text)
    return txt

def strip_tags(txt: str) -> str:
    s = BeautifulSoup(txt,"html.parser")
    return s.get_text()

def stemming(emailText: str) -> str:
    stopWords = set(nltk.corpus.stopwords.words("english"))
    wordTokens = nltk.word_tokenize(emailText)
    filteredEmailText = [word for word in wordTokens if word.lower() not in stopWords]
    filteredEmailText = " ".join(filteredEmailText)
    return filteredEmailText

def emailParser(emailData: EmailData) -> pd.DataFrame:
    parser = HeaderParser()
    h = parser.parsestr(emailData.emailHeaders)
    body = emailData.emailBody

    pData = pd.DataFrame(data=h.values(), index=h.keys()).loc[
        ["From", "Subject", "To", "Return-Path", "Authentication-Results"]]

    emailDic = {
        "DKIM": -1,  # Checks whether the email passed the dkim check
        "SPF": -1,  # Checks whether the email passed the spf check
        "DMARC": -1,  # Checks whether the email passed the dmarc check
        "ARC": -1,  # Checks whether the email passed the arc check
        "Body dear word": -1,  # Checks whether the email has the "dear" word inside it
        "Body form": -1,  # Checks whether the email has a form html tag
        "Body html": -1,  # Checks whether the email contains html
        "Body button": -1,  # Checks whether the email has buttons
        "Number of Links": 0,  # Counts the number of links inside the email
        "Body Verify your account": -1,  # Checks whether the email contains the string "verify your account"
        "Body no of function words": 0,  # Counts the number of function words
        "From eq Return": -1,  # Checks whether the from address is equal to the reply address
        "Message-Id": h["Message-Id"],
    }

    functionWords = ["Account", "Access", "Bank", "Credit", "Click", "Identity", "Inconvenience", "Information",
                     "Limited", "Log", "Minutes", "Password", "Recently", "Risk", "Security", "Social", "Service",
                     "Suspended", "Urgent"]

    # Verify Dkim, spf, arc and dmarc passes
    for arcMsg in pData.loc["Authentication-Results"]:
        if "dkim=pass" in arcMsg:
            emailDic["DKIM"] = 1
        if "spf=pass" in arcMsg:
            emailDic["SPF"] = 1
        if "dmarc=pass" in arcMsg:
            emailDic["DMARC"] = 1
        if "arc=pass" in arcMsg:
            emailDic["ARC"] = 1

    # Verify body html,form button and verifyAcc
    html, dear, form, button, verifyAcc = containsWrapper("<style", body), containsWrapper("dear", body.lower()), containsWrapper("<form", body), containsWrapper("<button", body), containsWrapper("Verify your account", body.lower())
    myValues = [html, dear, form, button, verifyAcc]
    myKeys = ["Body html", "Body form", "Body dear word", "Body button", "Body Verify your account"]

    for x, y in zip(myKeys, myValues):
        emailDic[x] = y

    # Verify if "from" addr eq to "return" addr
    searchVal = re.search(r"<\s*(.*?)\s*>", str(pData.loc["From"].values))

    if searchVal:
        fromAddress = searchVal.group(1)
    else:
        fromAddress = "None"

    if fromAddress == pData.loc["Return-Path"][0]:
        emailDic["From eq Return"] = 1

    # Count the number of links by counting the number of href tags in html code
    emailDic["Number of Links"] += body.lower().count("http")

    # Count the number of function words inside the email
    for word in functionWords:
        if body.lower().find(word.lower()) != -1:
            emailDic["Body no of function words"] += 1

    # Remove tags, punctuation and stem the body message
    body = stemming(remove_punct(strip_tags(body)))

    #Load the data into a pd DataFrame
    modelData = pd.DataFrame([emailDic])
    modelData.set_index("Message-Id", inplace=True)
    modelData["Text"] = body
    return modelData



########
# Parse through the list and get all the received headers in order of the email route
########

# def getReceivedHeaders() -> dict:
#     rcvList = dict()
#     index: int = 0
#     for key in msg.keys():
#         if key == 'Received':
#             rcvList[index] = msg.values().pop(index)
#         index += 1
#     return rcvList
