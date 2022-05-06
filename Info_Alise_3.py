from db_working import *
import pymorphy2
import random

morph = pymorphy2.MorphAnalyzer()

words = ['а', 'банк', 'всем', 'выведи', 'дай', 'ещё', 'им', 'инфо', 'информ', 'информацию',
         'информация', 'которые', 'который', 'кошел', 'кошелек', 'кошельке', 'кошельки',
         'мне', 'на', 'называется', 'название', 'названием', 'названиями', 'называются',
         'нам', 'о', 'об', 'по', 'пожалуйста', 'пока', 'привет', 'про', 'про',
         'расскажи', 'с', 'спасибо', 'счет', 'счета', 'счете', 'счету', 'счёт',
         'счёте', 'счёту']

variations1 = ['Информация о каком кошельке вам нужна? ',
               'О каком кошельке вы хотите узнать?' ,
               'Не расслышал, какой кошелёк вам интересен? ',
               'Извините, какой кошелёк вы имели ввиду? ']

variations2 = ['По моему, такого кошелька нет. ',
               'Что-то не нашёл такого кошелька. ',
               'Вы правильно указали кошелёк? ']

other_frase = 'Если вы хотите узнать имена всех своих кошельков, скажите "выведи все мои кошельки".'


def information(general_frase, user_name, k):
    main_words = []
    person_data = from_db('users', 'Users', {'username': user_name})
    base = from_db('accounts', 'Accounts', {'user_id': person_data[0].id})
    all_accounts = [str(akk.accounts) for akk in from_db('accounts', 'Accounts', {'user_id': person_data[0].id})]
    if len(all_accounts) == 0:
        return 'У вас пока нет счетов.', {}
    accounts_data = [q.accounts for q in base]
    main_frase = (general_frase.split())
    main_words = [word for word in main_frase if word not in words]

    if k == {}:
        if len(main_words) == 0:
            return random.choice(variations1) + other_frase, {'name': 0}
        else:
            for i in main_words:
                for q in accounts_data:
                    if i in q.split():
                        norm_fr = morph.parse(base[accounts_data.index(q)].currency)
                        variations02 = [f'На этом счету ',
                                        f'На счету {q} ',
                                        f'На счету кошелька {q} ',
                                        f'В кошельке {q} ',
                                        f'В этом кошельке ']
                        return random.choice(variations02) + str(base[accounts_data.index(q)].bank) + ' ' + norm_fr[0].make_agree_with_number(base[accounts_data.index(q)].bank).word, {}
            return random.choice(variations2) + other_frase, {}
    elif k['name'] == 0:
        if len(main_words) == 0:
                return random.choice(variations1) + other_frase, {'name': 0}
        else:
            for i in main_words:
                for q in accounts_data:
                    if i in q.split():
                        norm_fr = morph.parse(base[accounts_data.index(q)].currency)
                        variations12 = [f'На этом счету ',
                                        f'На счету {q} ',
                                        f'На счету кошелька {q} ',
                                        f'В кошельке {q} ',
                                        f'В этом кошельке ']
                        return random.choice(variations12) + str(base[accounts_data.index(q)].bank) + norm_fr[0].make_agree_with_number(base[accounts_data.index(q)].bank).word, {}

                return random.choice(variations2) + other_frase, {}

#print(information('выведи информацию о счёте нигга', 'Test2', {}))
