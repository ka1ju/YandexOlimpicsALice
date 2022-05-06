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

variations1 = ['Информация о каком кошельке вам нужна? У вас есть счета: ',
               'О каком кошельке вы хотите узнать? У вас есть счета: ',
               'Не расслышал, какой кошелёк вам интересен? У вас есть счета: ',
               'Извините, какой кошелёк вы имели ввиду? У вас есть счета: ']

variations2 = [f'По моему, такого кошелька нет. У вас есть счета: ',
               f'Что-то не нашёл такого кошелька. У вас есть счета: ',
               f'Вы правильно указали кошелёк? У вас есть счета: ']

and_other = ' и другие. Если вы хотите узнать имена всех своих кошельков, скажите "выведи все мои кошельки".'


def information(general_frase, user_name, k):
    main_words = []
    person_data = from_db('users', 'Users', {'username': user_name})
    base = from_db('accounts', 'Accounts', {'user_id': person_data[0].id})
    all_accounts = [str(akk.accounts) for akk in from_db('accounts', 'Accounts', {'user_id': person_data[0].id})]
    if len(all_accounts) == 0:
        return 'У вас пока нет счетов.', {}
    accounts_data = [q.accounts for q in base]
    main_frase = (general_frase.split())
    for word in main_frase:
        if word not in words:
            main_words.append(word)
    if k == {}:
        if len(main_words) == 0:
            if len(all_accounts) > 3:
                _words = ', '.join(all_accounts[:3])
                return random.choice(variations1) + _words + and_other, {'name': 0}
            else:
                _words = ', '.join(all_accounts)
                return random.choice(variations1) + _words + '.', {'name': 0}
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
            if len(all_accounts) > 3:
                _words = ', '.join(all_accounts[:3])
                return random.choice(variations2) + _words + and_other, {}
            else:
                _words = ', '.join(all_accounts)
                return random.choice(variations2) + _words, {}
    elif k['name'] == 0:
        if len(main_words) == 0:
            if len(all_accounts) > 3:
                _words = ', '.join(all_accounts[:3])
                return random.choice(variations1) + _words + and_other, {'name': 0}
            else:
                _words = ', '.join(all_accounts)
                return random.choice(variations1) + _words, {'name': 0}
        else:
            for i in main_words:
                for q in accounts_data:
                    if i in q.split():
                        norm_fr = morph.parse(base[accounts_data.index(q)].currency)
                        variations12 = ['На этом счету ',
                                        f'На счету {q} ',
                                        f'В кошельке ']
                        return random.choice(variations12) + str(base[accounts_data.index(q)].bank) + norm_fr[0].make_agree_with_number(base[accounts_data.index(q)].bank).word, {}
            if len(all_accounts) > 3:
                _words = ', '.join(all_accounts[:3])
                return random.choice(variations2) + _words + and_other, {}
            else:
                _words = ', '.join(all_accounts)
                return random.choice(variations2) + _words, {}

# n print(information('выведи информацию о счёте', 'Test2', {}))
