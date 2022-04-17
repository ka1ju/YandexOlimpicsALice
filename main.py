import json

f = open('funcs.json', 'r', encoding='utf-8')
x = json.load(f)
for i in x:
    print(i + ':')
    print('\tПояснение:', x[i][0])
    print('\tОбращение к Алисе:', x[i][1][0])
    print('\tПояснения к переменым:', *x[i][1][1], '\n')
