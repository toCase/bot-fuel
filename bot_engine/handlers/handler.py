from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from aiogram.fsm.context import FSMContext

from bot_engine.config import load_config
from bot_engine.keyboards import keyboard
from bot_engine.misc import fuel_connector

router=Router()
config=load_config('.env')

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    messa = '''Вітаю, це бот <b>GDT-SERVICE FUEL</b>. 
            Інформую про залишкі на паливному рахунку ОККО.
            Для отриvання інформації жміть INFO. 
            <i>Час очікування відповіді 20-30 сек</i>'''
    await message.answer(messa, reply_markup=keyboard.keyboard_start())

@router.message(F.text.lower() == 'info')
async def cmd_fuel(message: Message):
    messa = fuel_connector.get_info()
    await  message.answer(messa, reply_markup=keyboard.keyboard_start())

@router.message()
async def get_all_message(message: Message, state: FSMContext):
    print("ChatID: ", message.chat.id)


