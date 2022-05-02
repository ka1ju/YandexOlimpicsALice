from db_working import *
import pymorphy2
import random

morph = pymorphy2.MorphAnalyzer()


def information(general_frase, user_name, k):
    if k == {}:
        person_data = from_db('users', 'Users', {'username': user_name})
        base1 = from_db('accounts', 'Accounts', {'user_id': person_data[0].id})
        main_frase = (general_frase.split())

        words = ['а', 'банк', 'всем', 'выведи', 'ещё', 'им', 'инфо', 'информ', 'информацию', 'информация',
                 'коплю', 'которые', 'который', 'кошел', 'кошельки', 'кошелёк', 'мне', 'на', 'на', 'назвается',
                 'название', 'названием', 'названиями', 'назваются', 'нам', 'по', 'пожалуйста', 'пока',
                 'привет', 'про', 'расскажи', 'с', 'спасибо', 'счета', 'счёт', 'счёту'
                 ]
        main_words = []

        for it in main_frase:
            if it not in words:
                main_words.append(it)

        if not main_words:
            all_accounts = [str(akk.accounts) for akk in from_db('accounts', 'Accounts')]
            if len(all_accounts) > 3:
                wordssss = ', '.join(all_accounts[:3])
            else:
                wordssss = ', '.join(all_accounts)
            variations01 = [f'Информация о каком кошельке вам нужна? У вас есть счета: {wordssss}',
                            f'О каком кошельке вы хотите узнать? У вас есть счета: {wordssss}',
                            f'Про что вы хотите узнать? У вас есть кошельки: {wordssss}',
                            f'Не расслышала, какой кошелёк вам интересен? У вас есть счета: {wordssss}',
                            f'Извините, не расслышала. Какой-какой кошелёк? У вас есть счета: {wordssss}'
                            ]
            return random.choice(variations01) + \
                '. Если вы хотите узнать имена всех своих кошельков, скажите "все мои кошельки".', {'name': 0}

        accounts_data = [q.accounts for q in base1]

        for i in main_words:
            for q in accounts_data:
                if i in q.split():
                    currency_normal_form = morph.parse(base1[accounts_data.index(q)].currency)
                    variations02 = [f'На этом счету {base1[accounts_data.index(q)].bank} ',
                                    f'На счету {q} {base1[accounts_data.index(q)].bank} ',
                                    f'На счету кошелька {q} {base1[accounts_data.index(q)].bank} ',
                                    f'В кошельке {q} {base1[accounts_data.index(q)].bank} ',
                                    f'В этом кошельке {base1[accounts_data.index(q)].bank} ',
                                    ]
                    return random.choice(variations02) + \
                        f'{currency_normal_form[0].make_agree_with_number(base1[accounts_data.index(q)].bank).word}', {}

        all_accounts = [str(akk.accounts) for akk in from_db('accounts', 'Accounts')]
        if len(all_accounts) > 3:
            wordssss = ', '.join(all_accounts[:3])
        else:
            wordssss = ', '.join(all_accounts)

        variations03 = [f'По моему, такого кошелька не существует. У вас есть счета: {wordssss}',
                        f'Что-то не нашла такого кошелька. У вас есть счета: {wordssss}',
                        f'Вы точно правильно указали кошелёк? У вас есть счета: {wordssss}'
                        ]
        return random.choice(variations03) + \
            '. Если вы хотите узнать имена всех своих кошельков, скажите "все мои кошельки".', {}

    elif k['name'] == 0:
        person_data = from_db('users', 'Users', {'username': user_name})
        base1 = from_db('accounts', 'Accounts', {'user_id': person_data[0].id})
        main_frase = (general_frase.split())

        words = ['а', 'банк', 'всем', 'выведи', 'ещё', 'им', 'инфо', 'информ', 'информацию', 'информация',
                 'коплю', 'которые', 'который', 'кошел', 'кошельки', 'кошелёк', 'мне', 'на', 'назвается',
                 'название', 'названием', 'названиями', 'назваются', 'нам', 'по', 'пожалуйста', 'пока',
                 'привет', 'про', 'расскажи', 'с', 'спасибо', 'счета', 'счёт', 'счёту'
                 ]
        main_words = []

        for it in main_frase:
            if it not in words:
                main_words.append(it)

        if not main_words:
            all_accounts = [str(akk.accounts) for akk in from_db('accounts', 'Accounts')]
            if len(all_accounts) > 3:
                wordssss = ', '.join(all_accounts[:3])
            else:
                wordssss = ', '.join(all_accounts)
            variations11 = [f'Информация о каком кошельке вам нужна? У вас есть счета: {wordssss}',
                            f'О каком кошельке вы хотите узнать? У вас есть счета: {wordssss}',
                            f'Про что вы хотите узнать? У вас есть кошельки: {wordssss}',
                            f'Не расслышала, какой кошелёк вам интересен? У вас есть счета: {wordssss}',
                            f'Извините, не расслышала. Какой-какой кошелёк? У вас есть счета: {wordssss}'
                            ]
            return random.choice(variations11) + \
                '. Если вы хотите узнать имена всех своих кошельков, скажите "все мои кошельки".', {'name': 0}

        accounts_data = [q.accounts for q in base1]
        for i in main_words:
            for q in accounts_data:
                if i in q.split():
                    currency_normal_form = morph.parse(base1[accounts_data.index(q)].currency)
                    variations12 = [f'На этом счету {base1[accounts_data.index(q)].bank} ',
                                    f'На счету {q} {base1[accounts_data.index(q)].bank} ',
                                    f'На счету кошелька {q} {base1[accounts_data.index(q)].bank} ',
                                    f'В кошельке {q} {base1[accounts_data.index(q)].bank} ',
                                    f'В этом кошельке {base1[accounts_data.index(q)].bank} ',
                                    ]
                    return random.choice(variations12) + \
                        currency_normal_form[0].make_agree_with_number(base1[accounts_data.index(q)].bank).word, {}

        all_accounts = [str(akk.accounts) for akk in from_db('accounts', 'Accounts')]
        if len(all_accounts) > 3:
            wordssss = ', '.join(all_accounts[:3])
        else:
            wordssss = ', '.join(all_accounts)
        variations13 = [f'По моему, такого кошелька не существует. У вас есть счета: {wordssss}',
                        f'Что-то не нашла такого кошелька. У вас есть счета: {wordssss}',
                        f'Вы точно правильно указали кошелёк? У вас есть счета: {wordssss}'
                        ]
        return random.choice(variations13) + \
            '. Если вы хотите узнать имена всех своих кошельков, скажите "все мои кошельки".', {}


# print(information('выведи информацию по счёту одктпот', 'Test2', {}))
# 2.05.2022, 19:35, by Mr_Hamstr
