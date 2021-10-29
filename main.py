from PIL import Image
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import md
import config
from functions import transorm_photo, get_answer, crop_photo, return_photo_from_db
from model import model
from photo_with_mask import get_color
from furniture_correlator import correlate

bot = Bot(token=config.token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message):
    await bot.send_message(message.chat.id, 'Привет, этот бот умеет подбирать мебель под твою мебель.\n'
                                            'Просто отправь фото боту, и он автоматически ее подберет.\n'
                                            'P.s Желательно, чтобы мебель была в центре объектива(камеры) '
                                            'и крупным планом')


@dp.message_handler(lambda message: True)
async def echo_all(message):
    await bot.send_message(message.chat.id, f'Hi, {message.text}')


@dp.message_handler(content_types=['photo'])
async def echo_photo(message):
    try:
        file_info = await bot.get_file(message.photo[-1].file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        img = Image.open(downloaded_file)
        images_transormed = transorm_photo(img)
        img = crop_photo(img)
        color = get_color(img)
        answer = get_answer(model, images_transormed)
        result = correlate(answer, color)
        for i in result:
            photo = return_photo_from_db(i[1])
            await bot.send_message(message.chat.id, f'[Кликни, чтобы перейти на страницу товара]({i[0]})',
                                   parse_mode='markdown')
            await bot.send_photo(message.chat.id, photo=photo)
        photo.close()
    except Exception:
        await bot.send_message(message.chat.id, 'Неверный формат файла')


@dp.message_handler(content_types=['document'])
async def echo_photo(message):
    try:
        file_info = await bot.get_file(message.document.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)

        im = Image.open(downloaded_file)
        rgb_im = im.convert('RGB')
        rgb_im.save(f'photo/photo_{message.chat.id}.jpg')

        img = Image.open(f'photo/photo_{message.chat.id}.jpg')
        images_transormed = transorm_photo(img)
        img = crop_photo(img)
        color = get_color(img)
        answer = get_answer(model, images_transormed)
        result = correlate(answer, color)
        for i in result:
            photo = return_photo_from_db(i[1])
            await bot.send_message(message.chat.id, i[0])
            await bot.send_photo(message.chat.id, photo=photo)
        photo.close()
    except Exception:
        await bot.send_message(message.chat.id, 'Неверный формат файла')


if __name__ == '__main__':
    executor.start_polling(dp)
