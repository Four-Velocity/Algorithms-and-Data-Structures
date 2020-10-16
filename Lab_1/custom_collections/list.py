"""Містить реалізацию цілочисельного списку."""

from __future__ import annotations
from typing import Union


class CustomList:
    """Реалізація списку. Може містити лише int. Довжина може бути обмеженою."""

    def __init__(self, *elements: int, maxlen: int = 0):
        """
        Ініціалізація списку.

        Під час ініціалізації виконується перевірка типів елементів списку
        для впевненості що він містить лише цілі числа.
        :param elements: Цілочисленні лементи списку
        :param maxlen: Необов'язковий параметр.
        Дозволяє встановити максимальну довжину масиву.
        Якщо дорівнює 0 то кількість елементів необмежена.
        :raises TypeError: Якщо при ініціалізації у списку є не цілочисельний елемент.
        :raises ValueError: Якщо maxlen відємна
        :raises IndexError: Якщо кількість elements перевищує maxlen
        """
        if maxlen < 0:
            raise ValueError('maxlen must be a positive number ("not {}")'.format(maxlen))
        for element in elements:
            if not isinstance(element, int):
                raise TypeError(
                    'list can contain only int (not "{}")'.format(type(element).__name__)
                )
        if 0 < maxlen < len(elements):
            raise IndexError(
                "too many elements ({}) for list with maxlen {}".format(len(elements), maxlen)
            )
        self.elements = elements
        self.__maxlen = maxlen

    @property
    def maxlen(self) -> int:
        """
        Максимальна довжина списку.

        Приватний атрибут maxlen обгорнутий у property для того,
        щоб обмежити його модифікацію після того як екземляр класу створений.
        :return: Максимальна довжина списку
        """
        return self.__maxlen

    @maxlen.setter
    def maxlen(self, value: int):
        """
        Setter атрибуту maxlen.

        Забороняє змінювати максимальну довжину списку після створення.
        :param value: ...
        :raise AttributeError: При спробі змінити maxlen
        """
        raise AttributeError("max length is immutable, you can't change it")

    @maxlen.deleter
    def maxlen(self):
        """
        Deleter атрибуту maxlen.

        Забороняє видаляти максимальну довжину списку після створення.
        :raise AttributeError: При спробі видалити maxlen
        """
        raise AttributeError("max length is immutable, you can't delete it")

    def is_full(self) -> bool:
        """
        Перевіряє заповніність списку.

        :return: True: якщо список повний, або
                 False: якщо у списку ще є місце.
        """
        if not self.maxlen:
            return False
        else:
            return len(self) == self.maxlen

    def is_empty(self) -> bool:
        """
        Перевіряє заповніність списку.

        :return: True: якщо список пустий, або
                 False: якщо у списку є елементи.
        """
        return len(self) == 0

    def __str__(self) -> str:
        """
        Магічний метод. Дозволяє конвертувати список до рядка.

        :return: Список представлений як рядок.

        >>> new_cl = CustomList(1, 2, 3)
        >>> str(new_cl)
        "(1, 2, 3)"

        >>> new_cl = CustomList(1, 2, 3, maxlen=12)
        >>> str(new_cl)
        "(1, 2, 3) | Max Length is 12"
        """
        str_list = str(self.elements)
        if not self.maxlen:
            return str_list
        else:
            return f"{str_list} with max length {self.maxlen}"

    def __repr__(self):
        """
        Магічний метод. Дозволяє отримувати рядкове прадставлення списку.

        :return: Рядкова репрезентація екземпляру.

        >>> new_cl = CustomList(1, 2, 3)
        >>> repr(new_cl)
        "CustomList(1, 2, 3)"

        >>> new_cl = CustomList(1, 2, 3, maxlen=12)
        >>> repr(new_cl)
        "CustomList(1, 2, 3, maxlen=12)"
        """
        repr_list = str(self.elements)
        if not self.maxlen:
            return f"CustomList{repr_list}"
        else:
            return f"CustomList{repr_list[:-1]}, maxlen={self.maxlen})"

    def __add__(self, other: CustomList) -> CustomList:
        """
        Магічний метод. Дозволяє використовувати "+" між екземплярами класу для їх конкатенації.

        :param other: Еказемпляр CustomList який потрібно додати до поточного
        :return: Новий екземпляр класу що складається з поточного та класу що додається
        """
        if not isinstance(other, self.__class__):
            raise TypeError(
                'can only concatenate CustomList (not "{}") to CustomList'.format(
                    type(other).__name__
                )
            )
        if 0 in (self.maxlen, other.maxlen):
            maxlen = 0
        else:
            maxlen = self.maxlen + other.maxlen
        return CustomList(*(self.elements + other.elements), maxlen=maxlen)

    def __len__(self) -> int:
        """
        Магічний метод. Дозволяє отримувати довжину списку.

        Разом із __getitem__ автоматично реалізує ітератори.
        :return: Довжина списку.
        """
        return len(self.elements)

    def __getitem__(self, item: Union[int, slice]) -> Union[int, CustomList]:
        """
        Магічний метод. Дозволяє отримувати елементи списку.

        Разом із __len__ реалізує індексацію, зрізи, ітерацію
        та інші операції пов'язані з нею.
        :param item: Індекс або індекси елементів списку.
        :return: Елемент або декілька елементів списку.
        :raises IndexError: якщо індекс не входить у список.
        :raises TypeError: якщо індекс не відповідає необхідному типу данних.
        """
        if isinstance(item, int):
            try:
                return self.elements[item]
            except IndexError:
                raise IndexError("CustomList index out of range")
            except TypeError:
                raise TypeError(
                    "CustomList indices must be integers or slices, not {}".format(
                        type(item).__name__
                    )
                )

        else:
            return CustomList(*self.elements[item], maxlen=self.maxlen)
