import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6410598816:AAGtSrntFT24K19DWt169qnjkxva5u2iJJ4",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Меню"  # Можно менять текст
text_button_1 = "Автор"  # Можно менять текст
text_button_2 = "Помощь"  # Можно менять текст
text_button_3 = "Чем мы хороши"  # Можно менять текст


menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Здравствуйте! Это наша пиццерия 🖐',  # Можно менять текст
        reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Это наше вкуснейшее меню😄!Ознакомьтесь с ним: пицца пепперони, пицца 4 сыра и вкуснейшая маргарита!Выберите что вам понравилось и напишите о этом в чат 😋')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id,  '[ Чтобы заказать блюдо🍕🍕 нажмите на ссылку <-](https://yandex.com/)')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Спасибо за посещение бота!', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Автор этой пиццерии Тимка", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Это место помощи.Если возник вопрос как заказать блюдо после меню то просто напишите в чат то что вам понравилось в меню.После того как вы написали откроется ссылка на сайт там вы его и купите", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Мы хороши тем что делаем пиццу менее чем за 30 минут⏱!У нас только самые лучшие ингридиенты🍅🧀.И если возникнуть вопросы то мы обязательно ответим вам🖐 ", reply_markup=menu_keyboard)  # Можно менять текст


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()