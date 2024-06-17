from pydantic import BaseModel, StrictStr, EmailStr, Extra


class EmailData(BaseModel):
    email: EmailStr
    emailHeaders: StrictStr
    emailBody: StrictStr
    emailMessage: StrictStr

    class Config:
        extra = Extra.forbid
