from json import load


class CheckSellerFilter:


    def __call__(self, message) -> bool:
        with open('sellers_data.json') as file:
            data = load(file)
        return data['cur_seller'] == message.from_user.id

