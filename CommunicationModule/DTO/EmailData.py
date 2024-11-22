from pydantic import BaseModel, EmailStr, Extra, StrictStr


class EmailData(BaseModel):
    email: EmailStr
    emailHeaders: StrictStr
    emailBody: StrictStr
    emailMessage: StrictStr

    class Config:
        extra = Extra.forbid
