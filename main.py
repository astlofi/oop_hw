# В сети магазинов былы установлены кассы самообслуживания.
# Сеть магазинов огранизовала несколько вариантов акций:
# [Оплачено картой WorldPay(лучше названия не придумал)] Покупателю доступна скидка в размере 3% от суммы в чеке.
# [Скачано приложение магазина + Оформлена подписка "Тридцать один обед"] Покупателю доступна скидка в размере 10% от суммы выпечки и горячих напитков в чеке.
# [Скачано приложение магазина + Оформлена подписка "Месяц мяса"] Покупателю доступна скидка в размере 7% от суммы мяса в чеке

class DefaultBuy:
    def __init__(self):
        self.name = "name"

    def r_check(self, amount, card_name, is_app, check_list):
        if is_app:
            return self.app_cashback(self, amount, card_name, check_list)
        if not (is_app):
            return self.cashback(self, amount, card_name, check_list)

    def app_cashback(self, amount, card_name, check_list):
        return 0

    def cashback(self, amount, card_name, check_list):
        return 0


class AppBonus(DefaultBuy):
    def __init__(self):
        self.name = "Скачано приложение"

    def app_cashback(self, amount, card_name, check_list):
        return amount / 100 * 2  # процент скидки за приложение

    def cashback(self, amount, card_name, check_list):
        return 0


class CardSale(AppBonus):
    def __init__(self):
        self.name = "Оплачено картой"

    def app_cashback(self, amount, card_name, check_list):
        if card_name == "WorldPay":
            return super().app_cashback(self, amount, card_name,
                                        check_list) + amount / 100 * 3  # процент скидки по имени карты
        else:
            return super().app_cashback(self, amount, card_name, check_list)

    def cashback(self, amount, card_name, check_list):
        if card_name == "WorldPay":
            return super().cashback(self, amount, card_name,
                                    check_list) + amount / 100 * 3  # процент скидки по имени карты
        else:
            return super().cashback(self, amount, card_name, check_list)


class MeatSale(CardSale):
    def __init__(self):
        self.name = "Мясо"

    def SumMeat(self, c_list):
        sumM = 0
        for i in c_list:
            if i[1] == "meat":
                sumM += i[2]
        return sumM

    def app_cashback(self, amount, card_name, check_list):
        amount_meat = self.SumMeat(self, check_list)
        return super().app_cashback(self, amount, card_name,
                                    check_list) + amount_meat / 100 * 7  # процент скидки за мясо

    def cashback(self, amount, card_name, check_list):
        return super().cashback(self, amount, card_name,
                                check_list)  # т.к. данная акция может быть активна только с приложением


class BakeryAndHotDrinkSale(CardSale):
    def __init__(self):
        self.name = "Выпечка и горячие напитки"

    def SumBakeryAndHotDrink(self, c_list):
        sums = 0
        for i in c_list:
            if i[1] in ("bakery", "hot_drinks"):
                sums += i[2]
        print(sums)
        return sums

    def app_cashback(self, amount, card_name, check_list):
        amount_bakery_and_hot_drink = self.SumBakeryAndHotDrink(self, check_list)
        return super().app_cashback(self, amount, card_name,
                                    check_list) + amount_bakery_and_hot_drink / 100 * 10  # процент скидки за выпеч. и горяч. нап.

    def cashback(self, amount, card_name, check_list):
        amount_bakery_and_hot_drink = self.SumBakeryAndHotDrink(self, check_list)
        return super().cashback(self, amount, card_name,
                                check_list) + amount_bakery_and_hot_drink / 100 * 10  # процент скидки за выпеч. и горяч. нап.


class UserCheck:
    def __init__(self, amount, check_list, card_name, is_app, plan=None):
        self.amount = amount
        self.check_list = check_list
        self.is_app = is_app
        self.card_name = card_name
        self.plan = plan
        self._sum = None
        if self.plan == None:
            self.plan = DefaultBuy

    def __str__(self):
        return "Чек на {0._sum} рублей".format(self)

    @property
    def get_amount(self):
        return self._sum

    def result_amount(self):
        self._sum = self.amount - DefaultBuy.r_check(self.plan, self.amount, self.card_name, self.is_app,
                                                     self.check_list)


# Продукты, которые отсканировал клиент на кассе. Формируется как (Название, тип, цена).
check_products = (("Мясо", "meat", 50),
                  ("Пицца", "bakery", 50))
# После оплаты(sum([s[2] for s in check_products]) - сумма в чеке). Формируется как (Сумма в чеке, лист покупок, название банк. карты, скачано ли приложение магазина, какой вид скидок был выбран в магазине)
fedor = UserCheck(sum([s[2] for s in check_products]), check_products, "WordPay", True, MeatSale)
fedor.result_amount()

print(fedor)
