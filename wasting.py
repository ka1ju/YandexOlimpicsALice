from db_working import to_db, from_db, change_db, remove_from_db


def wasting(s, user_name):
    list = [('развлечения', []), ('продукты', []), ('налоги', []), ('магазины', []), ('другое', [])]
    user_id1 = [i.id for i in from_db("users", "Users", {"Username": user_name})]
    user_id = user_id1[0]
    N = ''
    x = 0
    t = ''
    a = s.split()
    for i in range(0, len(a)):
        if ord('0') <= ord(a[i][0]) <= ord('9'):
            x = a[i]
    names = [i.account for i in from_db("accounts", "Accounts", {"user_id": user_id})]
    for i in range(len(names)):
        names[i] = names[i][0:-3]
    for i in a:
        if i[0:-3] in names:
            N = i
            break



    id1 = [i.id for i in from_db("accounts", "Accounts", {"account": N, "user_id": user_id})]
    id = id1[0]
    summ1 = [j.bank for j in from_db("accounts", "Accounts", {"account": N, "user_id": user_id})]
    summ = summ1[0]
    summ -= x
    newcount1 = [k.count for k in from_db("waste", "Waste", {"account_id": id, "category": t})]
    newcount = newcount1[0]
    newcount += x
    change_db("accounts", "Accounts", {"bank": summ}, {"account": N, "user_id": user_id})
    change_db("waste", "Waste", {"count": newcount}, {"account_id": id, "category": t})
# N - название счёта, x - сумма, t - категория
# частично сделал распознавание
