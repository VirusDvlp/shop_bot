from config import db


def count_basket_total(basket: list):
    total = 0
    for good in basket:
        if good == '':
            continue
        total += db.get_good_price(good)
    return total
