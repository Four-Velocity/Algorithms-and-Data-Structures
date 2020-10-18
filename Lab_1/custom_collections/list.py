"""Містить реалізацию цілочисельного списку."""

from __future__ import annotations
from typing import Union, Iterable, Optional


class CustomList:
    """Реалізація списку. Може містити лише int. Довжина може бути обмеженою."""

    def __init__(self, *elements: int, maxlen: int = 0):
        """
        Ініціалізація списку.

        Під час ініціалізації виконується перевірка типів елементів списку
        для впевненості що він містить лише цілі числа.
        :param elements: ціло численні елементи списку.
        :param maxlen: необов'язковий параметр.
        Дозволяє встановити максимальну довжину масиву.
        Якщо дорівнює 0 то кількість елементів необмежена.
        :raises TypeError: якщо при ініціалізації у списку є не цілочисельний елемент.
        :raises ValueError: якщо maxlen від'ємна.
        :raises OverflowError: якщо кількість elements перевищує maxlen.
        """
        if maxlen < 0:
            raise ValueError('maxlen must be a positive number ("not {}")'.format(maxlen))
        for element in elements:
            if not isinstance(element, int):
                raise TypeError(
                    'list can contain only int (not "{}")'.format(type(element).__name__)
                )
        if 0 < maxlen < len(elements):
            raise OverflowError(
                "too many elements ({}) for list with maxlen {}".format(len(elements), maxlen)
            )
        self.elements = elements
        self.__maxlen = maxlen

    @property
    def maxlen(self) -> int:
        """
        Максимальна довжина списку.

        Приватний атрибут maxlen обгорнутий у property для того,
        щоб обмежити його модифікацію після того як екземпляр класу створений.

        :return: максимальна довжина списку.
        """
        return self.__maxlen

    @maxlen.setter
    def maxlen(self, value: int):
        """
        Setter атрибуту maxlen.

        Забороняє змінювати максимальну довжину списку після створення.

        :param value: ...
        :raise AttributeError: при спробі змінити maxlen.
        """
        raise AttributeError("max length is immutable, you can't change it")

    @maxlen.deleter
    def maxlen(self):
        """
        Deleter атрибуту maxlen.

        Забороняє видаляти максимальну довжину списку після створення.

        :raise AttributeError: при спробі видалити maxlen.
        """
        raise AttributeError("max length is immutable, you can't delete it")

    def is_full(self) -> bool:
        """
        Перевіряє заповненість списку.

        :return: True: якщо список повний, або
                 False: якщо у списку ще є місце.
        """
        if not self.maxlen:
            return False
        else:
            return len(self) == self.maxlen

    def is_empty(self) -> bool:
        """
        Перевіряє заповненість списку.

        :return: True: якщо список пустий, або
                 False: якщо у списку є елементи.
        """
        return len(self) == 0

    def append(self, x: int):
        """
        Додає елемент х у кінець списку.

        :param x: число яке потрібно додати.
        :raises TypeError: якщо x не цілочисельний елемент.
        :raises OverflowError: якщо список повний і місця для нового елементу нема.
        """
        if self.is_full():
            raise OverflowError("list is full")
        if not isinstance(x, int):
            raise TypeError('list can contain only int (not "{}")'.format(type(x).__name__))
        self.elements += x

    def extend(self, iterable: Iterable[int]):
        """
        Додає елементи з iterable у кінець списку.

        :param iterable: колекція елементів які потрібно додати.
        :raises TypeError: якщо один з елементів не цілочисельний.
        :raises OverflowError: якщо список повний і місця для нового елементу нема.
        """
        for element in iterable:
            if self.is_full():
                raise OverflowError("list is full")
            if not isinstance(element, int):
                raise TypeError(
                    'list can contain only int (not "{}")'.format(type(element).__name__)
                )
            self.elements += element

    def pop(self, index: int = -1) -> int:
        """
        Видаляє елемент зі списку по індексу та повертає його значення.

        Якщо індекс не вказано видаляє останній елемент.

        :param index: індекс елементу який видаляється зі списку.
        :return: значення видаленого елемента.
        :raises IndexError: якщо список пустий.
        """
        if self.is_empty():
            raise IndexError("CustomList index out of range")
        if index == -1 or index == self.__len__() - 1:
            element = self.__getitem__(-1)
            self.elements = self.elements[:-1]
        elif index == 0:
            element = self.__getitem__(0)
            self.elements = self.elements[1:]
        else:
            element = self.__getitem__(index)
            self.elements = self.elements[:index] + self.elements[index + 1 :]
        return element

    def clear(self):
        """Очищує список."""
        self.elements = ()

    def count(self, x: int) -> int:
        """
        Повертає кількість входжень елемента у списку.

        :param x: елемент, кількість якого необхідно підрахувати.
        :return: кількість входжень елемента.
        """
        counter = 0
        for element in self.elements:
            if element == x:
                counter += 1
        return counter

    def index(self, x: int, start: int = 0, stop: int = -1) -> Optional[int]:
        """
        Повертає індекс першого входження елементу.

        Повертає None, якщо елемент у списку відсутній.
        Можна задати значення start або stop для пошуку у зрізі зі списку.
        :param x: значення індекс якого потрібно знайти.
        :param start: індекс початку пошуку.
        :param stop: індекс завершення пошуку.
        :return: індекс першого входження елементу, або None, якщо елементу нема у списку.
        """
        for index, element in enumerate(self.elements[start:stop], start):
            if element == x:
                return index
        return None

    def insert(self, element: int, index: int):
        """
        Вставляє елемент на вказану позицію.

        :param element: значення елементу, який необхідно вставити.
        :param index: позиція на яку потрібно вставити елемент.
        """
        self.elements = self.elements[:index] + (element,) + self.elements[index:]

    def reverse(self):
        """Відзеркалює список."""
        self.elements = self.elements[::-1]

    def __str__(self) -> str:
        """
        Магічний метод. Дозволяє конвертувати список до рядка.

        :return: список представлений як рядок.

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

        :return: рядкова репрезентація екземпляру.

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

        :param other: екземпляр CustomList який потрібно додати до поточного.
        :return: Новий екземпляр класу що складається з поточного та класу що додається.
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
        :return: довжина списку.
        """
        return len(self.elements)

    def __getitem__(self, item: Union[int, slice]) -> Union[int, CustomList]:
        """
        Магічний метод. Дозволяє отримувати елементи списку.

        Разом із __len__ реалізує індексацію, зрізи, ітерацію
        та інші операції пов'язані з нею.
        :param item: індекс або індекси елементів списку.
        :return: Елемент або декілька елементів списку.
        :raises IndexError: якщо індекс не входить у список.
        :raises TypeError: якщо індекс не відповідає необхідному типу даних.
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
