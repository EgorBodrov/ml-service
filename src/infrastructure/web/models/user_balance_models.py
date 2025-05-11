from pydantic import BaseModel


class UserBalanceResponse(BaseModel):
    amount: int


class UserBalanceRequest(BaseModel):
    new_amount: int
