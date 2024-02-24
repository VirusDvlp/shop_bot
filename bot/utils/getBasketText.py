from config import db



def get_basket_text(basket, gt, total) -> str:
    uniq_basket = set(basket)
    text = 'Сумма: ' + total +'руб\nКорзина:\n'
    for good in uniq_basket:
        if good == '':
            continue
        gd = db.get_good_data(good)
        text += f'{gd["name"]} - {basket.count(good)} шт\n'
    
    text += '\nСпособ получения:'
    text += 'доставка' if gt == 1 else 'в магазине'
    if gt == 1:
        text += '\nАдрес доставки:'
    return text
