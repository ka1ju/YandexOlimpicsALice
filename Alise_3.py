from db_working import *


def information(general_frase, user_name):
    global rar
    rar = False
    a = from_db('users', 'Users', {'username': user_name})
    base1 = from_db('accounts', 'Accounts', {'user_id': a[0].id})
    main_frase = (general_frase.lower().split())

    main_words = []
    words = ["кошел", "счёт", "счета", "кошелёк", "кошельки", "с", "на", "названием", "название", "названиями",
             "который", "которые", "назваются", "назвается", "привет", "пожалуйста", "пока", "спасибо", "а", "ещё",
             "расскажи", "нам", "им", "мне", "всем", "про", "банк", "инфо", "информ", "информация", "информацию"
             ]
    for it in main_frase:
        if it not in words:
            main_words.append(it)

    for q in base1:
        for i in main_words:
            if i in q.accounts:
                print(f'На счету кошелька {i} находится {base1[0].bank} {base1[0].currency}')
                rar = True
                break
        break

    if not rar:
        print(f'Такого счёта не существует. У вас есть счета {[str(a.accounts) for a in base1]}')


information('Расскажи мне про счёт альфабанк', 'Test2')
