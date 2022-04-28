from db_working import *


def information(general_frase, user_name):
    no_account = True
    person_data = from_db('users', 'Users', {'username': user_name})

    if len(person_data) == 0:
        return 'Извините, данных по вашему аккаунту нет. Хотите завести кошелёк?'

    all_users = [str(abuser.username) for abuser in from_db('users', 'Users')]
    if user_name not in all_users:
        return 'Извините, я не узнала ваш голос, хотите завести аккаунт?'

    else:
        base1 = from_db('accounts', 'Accounts', {'user_id': person_data[0].id})

        main_frase = (general_frase.split())

        words = ["кошел", "кошелёк", "кошельки", "счёт", "счета", "с", "на", "названием", "название", "названиями",
                 "который", "которые", "назваются", "назвается", "привет", "пожалуйста", "пока", "спасибо", "а", "ещё",
                 "расскажи", "нам", "им", "мне", "всем", "про", "банк", "инфо", "информ", "информация", "информацию",
                 'коплю', "на"
                 ]

        main_words = []
        for it in main_frase:
            if it not in words:
                main_words.append(it)

        accounts_data = [q.accounts for q in base1]

        for i in main_words:
            for q in accounts_data:
                if i in q.split():
                    no_account = False
                    return f'На счету кошелька {q} находится {base1[accounts_data.index(q)].bank}' \
                           f' {base1[accounts_data.index(q)].currency}'

        if no_account:
            all_accounts = [str(akk.accounts) for akk in from_db('accounts', 'Accounts')]
            return f'Такого счёта не существует. У вас есть счета: {all_accounts}'


print(information('Расскажи мне про счёт коплю на мечту', 'Test2'))
