from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token:str
    chat:str

@dataclass
class FuelAcc:
    f_login:str
    f_pass:str

@dataclass
class Config:
    tg_bot: TgBot
    fuel_acc: FuelAcc

def load_config(path :str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("TOKEN"),
            chat=env.str("CHAT")
        ),
        fuel_acc=FuelAcc(
            f_login=env.str("LOGIN"),
            f_pass=env.str("PASSWORD"),
        ),
    )