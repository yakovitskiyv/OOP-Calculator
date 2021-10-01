"""
"Этот модуль посчитывает количество потраченных денег
за сегодня и последние семь дней, с рассчетом остатка или долга
в трех валютах: рублях, долларах США, Евро,
а так же подсчитывает количество потребленных калорий
за сегодня и последние 7 дней.
Модуль дает пользователю советы, взависимости от состояния
остатка денег и непотребленных каллорий.

"""


import datetime as dt
from typing import Optional, Union


class Calculator:
    """
    Родительский класс с базовым функционалом
    get_today_stats и get_week_stats.
    """
    def __init__(self, limit: Union[int, float]) -> None:
        self.limit = limit
        self.records: list = []

    def add_record(self, record: 'Record') -> None:
        """Добавляет запись в словарь Records"""
        self.records.append(record)

    def get_today_stats(self) -> Union[int, float]:
        """
        Возвращает статистику за сегодня
        (Переделано через генератор списка с условием по замечанию ревьюера)
        """
        current_date = dt.date.today()
        return round(sum(float(rec.amount)
                         for rec in self.records
                         if rec.date == current_date), 2)

    def get_week_stats(self) -> Union[int, float]:
        """
        Возвращает статистику за последние семь дней
        (Переделано через генератор списка с условием по замечанию ревьюера).
        """
        current_date = dt.date.today()
        date_seven_day_back = current_date - dt.timedelta(days=7)
        result = sum(
            float(rec.amount) for rec in self.records
            if date_seven_day_back < rec.date <= current_date
        )
        return round(result, 2)

    def today_remained(self) -> Union[int, float]:
        """
        Возвращает остаток не использованного лимита за сегодня
        (Помещено в родительский класс по замечанию ревьюера).
        """
        return round(self.limit - self.get_today_stats(), 2)


class CaloriesCalculator(Calculator):
    """
    Дочерний класс с базовым и расширенным функционалом
    get_calories_remained.
    """

    def get_calories_remained(self) -> str:
        """
        Возвращает статистику за сегодня
         по остатку непотребленных калорий
        """
        today_calories_remained: float = round(
            self.today_remained()
        )

        if today_calories_remained <= 0:
            return 'Хватит есть!'
        return (
            'Сегодня можно съесть что-нибудь ещё, но с общей '
            f'калорийностью не более {today_calories_remained} кКал'
        )


class CashCalculator(Calculator):
    """
    Дочерний класс с базовым и расширенным функционалом
    get_calories_remained.
    """
    USD_RATE: float = 77.98
    EURO_RATE: float = 92.07

    def get_today_cash_remained(self, currency: str) -> str:
        """
        Возвращает статистику за сегодня по остатку непотраченных денег
        или долга в трех валютах: рублях, долларах США, Евро
        """
        self.CURRENCIES = {
            'rub': ('руб', 1),
            'usd': ('USD', float(self.USD_RATE)),
            'eur': ('Euro', float(self.EURO_RATE))
        }

        if currency not in self.CURRENCIES:
            return f'{currency} валюта не известна'

        today_cash_remained: float = self.today_remained()
        if today_cash_remained == 0:
            return 'Денег нет, держись'

        currency_name, currency_rate = self.CURRENCIES[currency]
        today_cash_remained = (
            round(
                today_cash_remained / currency_rate,
                2
            )
        )

        if today_cash_remained > 0:
            return f'На сегодня осталось {today_cash_remained} {currency_name}'
        return (
            'Денег нет, держись: твой долг - '
            f'{abs(today_cash_remained)} {currency_name}')


class Record:
    """ Класс для хранения типа данных Record. """

    def __init__(self, amount: Union[int, float],
                 comment: Optional[str] = 'Нет комментария',
                 date: Union[str, dt.date, None] = None) -> None:

        self.amount: Union[int, float] = amount
        self.comment: Optional[str] = comment
        self.date: Union[str, dt.date, None] = date

        if isinstance(date, str):
            format_record_date: str = '%d.%m.%Y'
            self.date = dt.datetime.strptime(date, format_record_date).date()
        if self.date is None:
            self.date = dt.date.today()


# Тестируем модуль.
if __name__ == '__main__':
    # Примеры записей.
    r1 = Record(amount=10, date='09.03.2021')
    r2 = Record(amount=10, comment='Запись 2', date='02.04.2021')
    r3 = Record(amount=10, comment='Запись 3', date='06.04.2021')
    r4 = Record(amount=10, comment='запись 4', date='07.04.2021')
    r5 = Record(amount=10, comment='запись 5', date='08.04.2021')
    r6 = Record(amount=10, comment='запись 6', date='09.04.2021')
    r7 = Record(amount=10.16339999, comment='запись 7', date='10.04.2021')
    r8 = Record(amount=10, comment='запись 8', date='12.04.2021')
    r9 = Record(amount=10.5465476746464, comment='запись 9', date='12.04.2021')
    r10 = Record(amount=10, comment='запись 10')
    r11 = Record(amount=145, comment='кофе')
    r12 = Record(amount=300, comment='Серёге за обед')
    r13 = Record(amount=3000, comment='бар в Танин др', date='12.04.2021')
    r14 = Record(amount=1186,
                 comment='Кусок тортика. И ещё один.',
                 date='12.04.2021')
    r15 = Record(amount=84, comment='Йогурт.', date='12.04.2021')
    r16 = Record(amount=1140, comment='Баночка чипсов.', date='12.04.2021')

    # Создаем экземпляры классов:
    # Calculator, CaloriesCalculator(Calculator), CashCalculator(Calculator).
    C1 = Calculator(limit=1000)
    C2 = CaloriesCalculator(limit=10000)
    C3 = CashCalculator(limit=1000)

    # Тестируем метод add_record().
    C1.add_record(r1)
    C1.add_record(r2)
    C1.add_record(r3)
    C1.add_record(r4)
    C1.add_record(r5)
    C1.add_record(r6)
    C1.add_record(r7)
    C1.add_record(r8)
    C1.add_record(r9)
    C1.add_record(r10)

    C2.add_record(r1)
    C2.add_record(r2)
    C2.add_record(r3)
    C2.add_record(r4)
    C2.add_record(r5)
    C2.add_record(r6)
    C2.add_record(r7)
    C2.add_record(r8)
    C2.add_record(r9)
    C2.add_record(r10)
    C2.add_record(r11)
    C2.add_record(r12)
    C2.add_record(r13)

    C3.add_record(r1)
    C3.add_record(r2)
    C3.add_record(r3)
    C3.add_record(r4)
    C3.add_record(r5)
    C3.add_record(r6)
    C3.add_record(r7)
    C3.add_record(r8)
    C3.add_record(r9)
    C3.add_record(r10)
    C3.add_record(r14)
    C3.add_record(r15)
    C3.add_record(r16)

    # Смотрим, что получилось после работы метода add_record().
    for rec in C1.records:
        print(f' запись C1: {rec.date, rec.amount, rec.comment}')
    print('_____________________________________________________________')

    for rec in C2.records:
        print(f' запись C2: {rec.date, rec.amount, rec.comment}')
    print('_____________________________________________________________')
    for rec in C3.records:
        print(f' запись C3: {rec.date, rec.amount, rec.comment}')
    print('_____________________________________________________________')

    # Тестируем метод get_today_stats().
    print(f'C1.get_today_stats(): {C1.get_today_stats()}')
    print(f'C2.get_today_stats(): {C2.get_today_stats()}')
    print(f'C3.get_today_stats(): {C3.get_today_stats()}')

    # Тестируем метод get_calories_remained.
    print(f'C2.get_calories_remained: {C2.get_calories_remained()}')

    # Тестируем get_week_stats.
    print(f'C1.get_week_stats(): {C1.get_week_stats()}')
    print(f'C2.get_week_stats(): {C2.get_week_stats()}')
    print(f'C3.get_week_stats(): {C3.get_week_stats()}')

    # Тестируем метод get_today_cash_remained.
    print(
        f'C3.get_today_cash_remained(rub):{C3.get_today_cash_remained("rub")}')
    print(
        f'C3.get_today_cash_remained(usd):{C3.get_today_cash_remained("usd")}')
    print(
        f'C3.get_today_cash_remained(eur):{C3.get_today_cash_remained("eur")}')
    print(
        f'C3.get_today_cash_remained(хз):{C3.get_today_cash_remained("хз")}')
