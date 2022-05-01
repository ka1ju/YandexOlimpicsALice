from db_working import *
import pymorphy2
morph = pymorphy2.MorphAnalyzer()


def information(general_frase, user_name, k):
    if k == {}:
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
                     'коплю', "на",
                     ]
            main_words = []
            for it in main_frase:
                if it not in words:
                    main_words.append(it)

            if not main_words:
                return 'Информация о каком кошельке вам нужна?', {'name': 0}
            accounts_data = [q.accounts for q in base1]

            for i in main_words:
                for q in accounts_data:
                    if i in q.split():
                        currency_normal_form = morph.parse(base1[accounts_data.index(q)].currency)
                        return f'На счету кошелька {q} находится {base1[accounts_data.index(q)].bank} ' \
                               f'{currency_normal_form[0].make_agree_with_number(base1[accounts_data.index(q)].bank).word}'

            all_accounts = [str(akk.accounts) for akk in from_db('accounts', 'Accounts')]
            wordssss = ', '.join(all_accounts)
            return f'Такого счёта не существует. У вас есть счета: {wordssss}', {}
    elif k['name'] == 0:
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
                     "который", "которые", "назваются", "назвается", "привет", "пожалуйста", "пока", "спасибо", "а",
                     "ещё",
                     "расскажи", "нам", "им", "мне", "всем", "про", "банк", "инфо", "информ", "информация",
                     "информацию",
                     'коплю', "на",
                     ]
            main_words = []
            for it in main_frase:
                if it not in words:
                    main_words.append(it)

            if not main_words:
                return 'Информация о каком кошельке вам нужна?', {'name': 0}
            accounts_data = [q.accounts for q in base1]

            for i in main_words:
                for q in accounts_data:
                    if i in q.split():
                        currency_normal_form = morph.parse(base1[accounts_data.index(q)].currency)
                        return f'На счету кошелька {q} находится {base1[accounts_data.index(q)].bank} ' \
                               f'{currency_normal_form[0].make_agree_with_number(base1[accounts_data.index(q)].bank).word}'

            all_accounts = [str(akk.accounts) for akk in from_db('accounts', 'Accounts')]
            wordssss = ', '.join(all_accounts)
            return f'Такого счёта не существует. У вас есть счета: {wordssss}', {}



#print(information('расскажи мне про счёт коплю на мечту', 'Test2', {'name': 0}))
