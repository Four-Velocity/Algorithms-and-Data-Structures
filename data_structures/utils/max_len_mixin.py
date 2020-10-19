"""Реалізація службових класів та функцій."""

from typing import Any

__all__ = ["MaxLenMixin"]


class MaxLenMixin(object):
    """
    Розширює колекцію додаючи до неї максимальну довжину.

    Справжнє значення maxlen зберігається у приватному атрибуті класу, але доступно
    ззовні через property maxlen.
    Це зроблено для того щоб maxlen можна було встановити лише при створенні
    екземпляру класу.
    """

    def __init__(self, *elements: Any, maxlen: int):
        """
        Додає приватний атрибут __maxlen за допомогою якого працює property maxlen.

        :param elements: елементи колекції.
        :param maxlen: максимальна довжина колекції. 0 для довжини без обмежень.
        :raises ValueError: якщо maxlen від'ємна.
        """
        if maxlen < 0:
            raise ValueError('maxlen must be a positive number ("not {}")'.format(maxlen))
        self.__maxlen = maxlen
        self.__overflow_check(elements)

    @property
    def maxlen(self) -> int:
        """
        Максимальна довжина колекції.

        Приватний атрибут maxlen обгорнутий у property для того,
        щоб обмежити його модифікацію після того як екземпляр класу створений.

        :return: максимальна довжина колекції.
        """
        return self.__maxlen

    @maxlen.setter
    def maxlen(self, value: int):
        """
        Setter атрибуту maxlen.

        Забороняє змінювати максимальну довжину колекції після створення.

        :param value: ...
        :raise AttributeError: при спробі змінити maxlen.
        """
        raise AttributeError("max length is immutable, you can't change it")

    @maxlen.deleter
    def maxlen(self):
        """
        Deleter атрибуту maxlen.

        Забороняє видаляти максимальну довжину колекції після створення.

        :raise AttributeError: при спробі видалити maxlen.
        """
        raise AttributeError("max length is immutable, you can't delete it")

    def __overflow_check(self, elements: Any):
        """
        Перевіряє чи не перевищує кількість елементів максимальну довжину.

        :param elements: елементи колекції.
        :raises OverflowError: якщо кількість elements перевищує maxlen.
        """
        if 0 < self.__maxlen < len(elements):
            raise OverflowError(
                "too many elements ({}) for list with maxlen {}".format(
                    len(elements), self.__maxlen
                )
            )
