# smartshell_botpython
Бот написан для панели SMARTSHELL , бот предназначен для того что бы брать необходимую информацию с панели не заходя на сайт.

![image](https://github.com/kurkov1337/smartshell_botpython/assets/145959131/f237800f-e9e1-42fc-bd34-45ba7987303f)

Возможности бота: 
"Статус пк -  показывает вам информацию ID , МЕСТО, НАЗВАНИЕ , СОСТОЯНИЕ. Где ID это уникальный номер ПК, Место и Название показывает какой компьютер по счету и его название в  WINDOWS, Состояние: TRUE or False (Вкючен или выключен) По желанию можно добавить юзера который сидит за пк (если такой есть)"
"Магазин информация - показывает вам ID , Название , Цена продажи , Цена закупки , Наличие."
"Деньги на депозитах - Показывает общую сумму которая на балансах юзеров (клиентов)"
Информация про смену показывает вам - Имя сотрудника на смене, Заработок на смену , Номер телефона сотрудника, Дата/Время открытия смены"

Как настроить? 
Для начала вам необходимо выпусить токен telegram-бота. в боте @botfather 
После получить bearer-токен , его можно получить отправив сигнал на 
https://billing.smartshell.gg/api/graphql - с запросом -

mutation Login {
    login(input: { login: "ваш номер", password: "пароль", company_id: клуб id }) {
        token_type
        expires_in
        access_token
        refresh_token
    }
}

после получения ответа, копируем токен из запрсоа access_token. 

Заходим в main.py изменяем везде на свои ключи.

запускаем скрипт и все готово :) Кому не понятно пишите в телеграм - @neblant. 

Прощу соблюдать мой копирайт :) 





