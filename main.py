import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler
)

# Пожалуйста соблюдайте копирайт и не удаляйте ничего.
# KURKOFF PROJECT Версия 0.1.0 на момент публикации данного файла
# Не забывайте изменять токены перед словом Bearer (само bearer не трогать!!!)
# а так же изменить токен бота телеграм :) спасибо!!!
# Мануал как настроить бота в моем тг канаое: t.me/kurkoffproject , спасибо!

# Обработчик команды /start
async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("🖥 ПК", callback_data='info')],
        [InlineKeyboardButton("🛒 Магазин", callback_data='magazin')],
        [InlineKeyboardButton("💸 Общие депозиты", callback_data='deposit')],
        [InlineKeyboardButton("👨‍💻 Смена", callback_data='smena')],
        [InlineKeyboardButton("ℹ Полная версия", callback_data='faq')],

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('👋 Привет! Выбери интересующий пункт, для получения нужной информации.\n <a href="https://t.me/kurkoffproject">KURKOFF PROJECT</a> // Версия: 0.1.0', reply_markup=reply_markup, parse_mode="HTML")

# Обработчик нажатия на кнопку
async def button(update, context):
    query = update.callback_query

    if query.data == 'info':
        url = 'https://billing.smartshell.gg/api/graphql'
        headers = {
            'Authorization': 'Bearer ВАШ_ТОКЕН(BEARER НЕ УДАЛЯЕМ В НАЧАЛЕ)',
            'Content-Type': 'application/json'
        }
        body = """query Hosts {
    hosts {
        id
        group_id
        type_id
        position
        alias
        comment
        mac_addr
        ip_addr
        dns_name
        coord_x
        coord_y
        is_deleted
        in_service
        created_at
        shell_mode
        last_online
        online
        device_has_changed
        device_updated_at
        locked
        admin_called_at
    }
}
        """


        response = requests.post(url, headers=headers, json={"query": body})
        print(response.status_code)
        
        data = response.json()
        print(data)
        # Выводим информацию
        text = "=================================\n"
        for el in data["data"]["hosts"]:

            text += f"""🆔ID: {el["id"]}
🖥Место: {el["position"]}
📝Название: {el["alias"]}
🖥ДНС: {el["dns_name"]}
🟩/🟥Состояние: {el["online"]}
=================================
"""
        print(text)
        await query.edit_message_text(text)

    if query.data == 'magazin':
        url = 'https://billing.smartshell.gg/api/graphql'
        headers = {
            'Authorization': 'Bearer ВАШ_ТОКЕН(BEARER НЕ УДАЛЯЕМ В НАЧАЛЕ)',
            'Content-Type': 'application/json'
        }
        body = """query Goods {
    goods {
        id
        title
        subtitle
        comment
        cost
        wholesale_cost
        tax_percent
        unit_name
        unit_value
        amount
        image
        use_global_discounts
        created_at
        tax_system
        vat
        ean
        use_fair_sign
        is_excise
    }
}
        """


        response = requests.post(url, headers=headers, json={"query": body})
        print(response.status_code)
       
        data = response.json()
        print(data)
        # Выводим информацию
        text = "=================================\n"
        for el in data["data"]["goods"]:

            await context.bot.send_message(chat_id=query.message.chat_id,
                                     text = f"""🆔ID: {el["id"]}
📝Название: {el["title"]}
🟩Цена продажи: {el["cost"]} ₽
🟥Цена закупки: {el["wholesale_cost"]} ₽
🟦Наличие: {el["amount"]} ШТ
=================================
""")
        print(text)
        #await query.answer(data["data"]["goods"][0]["id"])

    if query.data == 'deposit':
        url = 'https://billing.smartshell.gg/api/graphql'
        headers = {
            'Authorization': 'Bearer ВАШ_ТОКЕН(BEARER НЕ УДАЛЯЕМ В НАЧАЛЕ)',
            'Content-Type': 'application/json'
        }
        body = """query Clients {
    clients {
        total_deposits
    }
}
        """


        response = requests.post(url, headers=headers, json={"query": body})
        print(response.status_code)

        data = response.json()
        print(data)
        # Выводим информацию

        text = f"Общая сумма на балансах: {data['data']['clients']['total_deposits']}"

        print(text)
        await query.edit_message_text(text)

    if query.data == 'smena':
        url = 'https://billing.smartshell.gg/api/graphql'
        headers = {
            'Authorization': 'Bearer ВАШ_ТОКЕН(BEARER НЕ УДАЛЯЕМ В НАЧАЛЕ)',
            'Content-Type': 'application/json'
        }
        body = """query ActiveWorkShift {
    activeWorkShift {
        id
        comment
        created_at
        finished_at
        worker {
            uuid
            login
            nickname
            phone
            email
            phone_suffix
            dob
            country_code
            first_name
            last_name
            middle_name
        }
        payments {
            sum
        }
    }
}
        """


        response = requests.post(url, headers=headers, json={"query": body})
        print(response.status_code)

        data = response.json()
        print(data)
        # Выводим информацию
        text = f"🧑‍💻Имя:{data['data']['activeWorkShift']['worker']['first_name']}"
        text_2 = f"🧑‍💻Фамилия:{data['data']['activeWorkShift']['worker']['last_name']}"
        text_3 = f"💰Наличные за сегодня:{data['data']['activeWorkShift']['payments'][0]['sum']}"
        text_4 = f"📲Номер телефона сотрудника:{data['data']['activeWorkShift']['worker']['phone']}"
        text_5 = f"⏰Открыл смену:{data['data']['activeWorkShift']['created_at']}"


        print(text)
        await context.bot.send_message(chat_id=query.message.chat_id, text=text)
        await context.bot.send_message(chat_id=query.message.chat_id, text=text_2)
        await context.bot.send_message(chat_id=query.message.chat_id, text=text_3)
        await context.bot.send_message(chat_id=query.message.chat_id, text=text_4)
        await context.bot.send_message(chat_id=query.message.chat_id, text=text_5)
        

    if query.data == 'faq':

        # Выводим информацию
        text = "Купить полную версию бота можно тут @kurkoffproject"

        print(text)
        await context.bot.send_message(chat_id=query.message.chat_id, text=text)
   
def main():

    # ДОСТУП БОТА :) НЕ ЗАБЫВАЕМ ВСТАВЛЯТЬ ТОКЕН
    application = Application.builder().token("токен_из_botfather").build()

    # Обработка команды /start
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
