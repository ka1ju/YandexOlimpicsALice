from db_working import *
import pymorphy2
import random
morph = pymorphy2.MorphAnalyzer()

words = ['а', 'балан', 'баланс', 'балансе', 'банк', 'всем', 'выведи', 'дай', 'из', 'им', 'инфо', 'информ',
         'информацию', 'информация', 'которые', 'который', 'кошел', 'кошелек', 'кошельке', 'кошельки',
         'мне', 'на', 'название', 'названием', 'названиями', 'называется', 'называются', 'нам', 'о',
         'об', 'по', 'пожалуйста', 'пока', 'привет', 'про', 'про', 'расскажи', 'с', 'спасибо', 'счет',
         'счета', 'счета', 'счете', 'счету', 'счёт', 'счёта', 'счёте', 'счёту']

variations1 = ['Баланс какого кошелька вам нужен? ',
               'О каком кошельке вы хотите узнать? ',
               'Не расслышал, какой кошелёк вам интересен? ',
               'Извините, какой кошелёк вы имели ввиду? ']

variations2 = ['По моему, такого кошелька нет. ',
               'Что-то не нашёл такого кошелька. ',
               'Вы правильно указали кошелёк? ']

variations3 = ['Ваш баланс: ',
                'На вашем балансе: ',
                'В этом кошельке: ',
                'В кошельке: ']

other_frase = 'Если вам нужны имена всех счетов, скажите: "выведи все мои кошельки".'


def information(general_frase, user_name, k):
    global variations02, variations12
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
                        if base[accounts_data.index(q)].currency == 'тенге':
                            return random.choice(variations3) + str(base[accounts_data.index(q)].bank) + ' тенге', {}
                        return random.choice(variations3) + str(base[accounts_data.index(q)].bank) + ' ' + \
                                norm_fr[0].make_agree_with_number(abs(base[accounts_data.index(q)].bank)).word, {}
            return random.choice(variations2) + other_frase, {}
    elif k['name'] == 0:
        if len(main_words) == 0:
            return random.choice(variations1) + other_frase, {'name': 0}
        else:
            for i in main_words:
                for q in accounts_data:
                    if i in q.split():
                        norm_fr = morph.parse(base[accounts_data.index(q)].currency)
                        if base[accounts_data.index(q)].currency == 'тенге':
                            return random.choice(variations3) + str(base[accounts_data.index(q)].bank) + ' тенге', {}
                        else:
                            return random.choice(variations3) + str(base[accounts_data.index(q)].bank) + ' ' + \
                               norm_fr[0].make_agree_with_number(abs(base[accounts_data.index(q)].bank)).word, {}

                return random.choice(variations2) + other_frase, {}


#print(information('выведи баланс счета 12', 'Test2', {"name":0}))