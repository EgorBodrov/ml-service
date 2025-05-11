from pydantic import BaseModel


class UserBalance(BaseModel):
    user_id: int
    amount: int = 0
