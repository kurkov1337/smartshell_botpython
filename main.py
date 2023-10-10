from aiogram import Dispatcher, Bot, types, executor

import requests

# Введите в строчку token - api бота (@botfather)
bot = Bot(token="TOKEN")
dp = Dispatcher(bot=bot)

# Теперь только тут обновлять Bearer-Token (после Bearer введите токен)
BEARER_TOKEN = "Bearer TOKEN"

# Обработчик команды /start
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text="🖥 ПК", callback_data="info"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            text="🛒 Магазин", callback_data="magazin"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            text="💸 Общие депозиты", callback_data="deposit"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            text="👨‍💻 Смена", callback_data="smena"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            text="ℹ Поддержка", callback_data="faq"
        )
    )

    # Отвечаем
    await message.answer("👋 Привет! Выбери интересующий пункт, для получения нужной информации. @kurkoffproject // Версия 0.1.9 Клуб: FREE CLUB",
                         reply_markup=keyboard)


# Обработчик кнопок
@dp.callback_query_handler()
async def give_info(callback: types.CallbackQuery):
    # клава с кнопкой "Меню"
    key_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_menu.add("Меню")
    await callback.answer()

    if callback.data == 'info':
        url = 'https://billing.smartshell.gg/api/graphql'
        headers = {
            'Authorization': BEARER_TOKEN,
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
        client_sessions {
            id
            duration
            elapsed
            total_cost
            status
            created_at
            started_at
            finished_at
            canceled_at
            client {
                nickname
            }
        }
    }
}"""

        response = requests.post(url, headers=headers, json={"query": body})
        print(response.status_code)

        data = response.json()
        print(data)
        # Выводим информацию
        text = "=================================\n"
        for el in data["data"]["hosts"]:
            print(el)
            text += f"""🆔ID: {el["id"]}
🖥Место: {el["position"]}
📝Название: {el["alias"]}
🖥ДНС: {el["dns_name"]}
🟩/🟥Состояние: {el["online"]}
👨‍💻Юзер за ПК: {"Нет" if len(el["client_sessions"]) == 0 else "Да"}
⏰Заверешние сеанса: {el["client_sessions"][0]["finished_at"] if len(el["client_sessions"]) != 0 else "Нету информации"}
    =================================
    """
        print(text)

        await callback.message.answer(text,
                                      reply_markup=key_menu)

    elif callback.data == 'magazin':
        url = 'https://billing.smartshell.gg/api/graphql'
        headers = {
            'Authorization': BEARER_TOKEN,
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
            await callback.message.answer(text=f"""🆔ID: {el["id"]}
📝Название: {el["title"]}
🟩Цена продажи: {el["cost"]} ₽
🟥Цена закупки: {el["wholesale_cost"]} ₽
🟦Наличие: {el["amount"]} ШТ
    =================================
    """)
        # print(text)


    elif callback.data == 'deposit':
        url = 'https://billing.smartshell.gg/api/graphql'
        headers = {
            'Authorization': BEARER_TOKEN,
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

        text = f"Общая сумма на балансах: {data['data']['clients']['total_deposits']} ₽"

        print(text)
        await callback.message.answer(text,
                                      reply_markup=key_menu)

    elif callback.data == 'smena':
        url = 'https://billing.smartshell.gg/api/graphql'
        headers = {
            'Authorization': BEARER_TOKEN,
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
        body_2 = """query Hosts {
    activeWorkShift {
        id
        comment
        created_at
        finished_at
        money {
            sum {
                cash
                card
                total
            }
        }
    }
}"""
        response = requests.post(url, headers=headers, json={"query": body})
        response_2 = requests.post(url, headers=headers, json={"query": body_2})
        data = response.json()
        data_work = response_2.json()
        print(response.status_code)

        print(data)
        print(data_work)
        # Выводим информацию
        text = f"""🧑‍💻Имя:{data['data']['activeWorkShift']['worker']['first_name']}
🧑‍💻Фамилия: {data['data']['activeWorkShift']['worker']['last_name']}
📲Номер телефона сотрудника:{data['data']['activeWorkShift']['worker']['phone']}
⏰Открыл смену: {data['data']['activeWorkShift']['created_at']}
💰Заработок за сегодня: {data_work["data"]["activeWorkShift"]["money"]["sum"]["total"]} ₽
💸Наличные: {data_work["data"]["activeWorkShift"]["money"]["sum"]["cash"]} ₽
💰Безналичные: {data_work["data"]["activeWorkShift"]["money"]["sum"]["card"]} ₽

        """

        print(text)
        await callback.message.answer(text,
                                      reply_markup=key_menu)

    if callback.data == 'faq':
        # Выводим информацию
        text = """===========<b>Поддержка</b>============
    <b>Поддержка - @kurkoffproject</b>
        """

        print(text)
        await callback.message.answer(text,
                                      reply_markup=key_menu,
                                      parse_mode="HTML")


# Обработчик кнопки "Меню"
@dp.message_handler(text="Меню")
async def cmd_menu(message: types.Message):
    # Создаём клаву и отправляем потом
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            text="🖥 ПК", callback_data="info"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            text="🛒 Магазин", callback_data="magazin"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            text="💸 Общие депозиты", callback_data="deposit"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            text="👨‍💻 Смена", callback_data="smena"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            text="Поддержка", callback_data="faq"
        )
    )

    await message.answer("👋 Привет! Выбери интересующий пункт, для получения нужной информации.\n@kurkoffproject // Версия 0.1.9 Клуб: FREE CLUB",
                         reply_markup=keyboard, parse_mode="HTML")


if __name__ == '__main__':
    # Запускаем бота
    executor.start_polling(dispatcher=dp, skip_updates=True)
