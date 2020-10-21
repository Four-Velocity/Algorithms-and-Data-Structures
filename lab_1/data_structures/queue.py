"""Містить реалізацію одно направленої черги та її конструктор."""

from __future__ import annotations
from typing import Any, Sequence, Iterable
from data_structures.utils import MaxLenMixin
from data_structures.utils.queue_exceptions import CustomQueueIsEmpty, CustomQueueIsFull

__all__ = ["CustomQueue"]


class CustomQueue(MaxLenMixin):
    """
    Реалізація одно направленої черги.

    Елементи входять з лівого боку та дістаються з правого.
    Може містити лише hex.
    Довжина може бути обмеженою.
    """

    def __init__(self, *elements: int, maxlen: int = 0):
        """
        Ініціалізація черги.

        Під час ініціалізації виконується конвертація числових елементів у hex.
        :param elements: ціло численні елементи черги.
        :param maxlen: необов'язковий параметр.
        Дозволяє встановити максимальну довжину черги.
        Якщо дорівнює 0 то кількість елементів необмежена.
        """
        self.elements = tuple(hex(element) for element in elements[::-1])
        print(self.elements)
        super(CustomQueue, self).__init__(*elements, maxlen=maxlen)

    def is_full(self) -> bool:
        """
        Перевіряє заповненість черги.

        :return: True: якщо черга повний, або
                 False: якщо у черзі ще є місце.
        """
        if not self.maxlen:
            return False
        else:
            return len(self) == self.maxlen

    def is_empty(self) -> bool:
        """
        Перевіряє заповненість черги.

        :return: True: якщо черга пустий, або
                 False: якщо у черзі є елементи.
        """
        return len(self) == 0

    def lpush(self, x: int):
        """
        Додає int елемент на початок черги.

        :param x: Елемент, який потрібно додати.
            Автоматично конвертує значення у hex.
        :raises CustomQueueIsFull: якщо черга заповнена.
        """
        self.lpush_hex(hex(x))

    def lpush_hex(self, x: str):
        """
        Додає hex елемент на початок черги.

        :param x: Елемент, який потрібно додати. Має бути hex.
        :raises CustomQueueIsFull: якщо черга заповнена.
        :raises ValueError: якщо значення hex некоректне.
        """
        if self.is_full():
            raise CustomQueueIsFull("queue is full")
        self._validate_hex(x)
        self.elements = (x,) + self.elements

    def rpop(self) -> str:
        """
        Видаляє останній елемент з черги та повертає його значення.

        :return: значення останнього елемента.
        :raises CustomQueueIsEmpty: якщо черга порожня.
        """
        if self.is_empty():
            raise CustomQueueIsEmpty("queue is empty")
        element = self.elements[-1]
        self.elements = self.elements[:-1]
        return element

    def rpop_int(self) -> int:
        """
        Видаляє останній елемент з черги та повертає його значення конвертоване в int.

        :return: значення останнього елемента конвертоване в int.
        :raises CustomQueueIsEmpty: якщо черга порожня.
        """
        return int(self.rpop(), 16)

    def lextend(self, iterable: Iterable[int]):
        """
        Додає декілька елементів на початок черги.

        Елементи додаються до черги в порядку їх появлення в iterable об'єкті.
        Фактично являє собою множинні self.lpush().
        :param iterable: ітерабельний об'єкт з числами.
        """
        for element in iterable:
            self.lpush(element)

    def lextend_hex(self, iterable: Iterable[str]):
        """
        Додає декілька елементів на початок черги.

        Елементи додаються до черги в порядку їх появлення в iterable об'єкті.
        Фактично являє собою множинні self.lpush_hex().
        :param iterable: ітерабельний об'єкт з хекс.
        """
        for element in iterable:
            self.lpush_hex(element)

    def clear(self, iterable):
        """Очищує чергу."""
        self.elements = ()

    def count(self, x: int) -> int:
        """
        Повертає кількість входжень числа у черзі. Автоматично конвертує x в хекс.

        :param x: елемент, кількість якого необхідно підрахувати.
        :return: кількість входжень елемента.
        """
        counter = 0
        hex_x = hex(x)
        for element in self.elements:
            if element == hex_x:
                counter += 1
        return counter

    def count_hex(self, x: str) -> int:
        """
        Повертає кількість входжень елемента у черзі.

        :param x: елемент, кількість якого необхідно підрахувати.
        :return: кількість входжень елемента.
        """
        counter = 0
        for element in self.elements:
            if element == x:
                counter += 1
        return counter

    def reverse(self):
        """
        Відзеркалює чергу.

        Фактично напрям черги не змінюється.
        Змінюється положення елементів у черзі.
        """
        self.elements = self.elements[::-1]

    def __str__(self):
        """
        Магічний метод. Дозволяє конвертувати список до рядка.

        :return: список представлений як рядок.
        """
        if self.maxlen:
            maxlen_suffix = f" with max length {self.maxlen}"
        else:
            maxlen_suffix = ""
        start = "("
        body = ""
        end = ")"
        for element in self.elements[:-1]:
            body += f"{element[2:].upper()} -> "
        try:
            body += self.elements[-1][2:].upper()
        except IndexError:
            pass
        return start + body + end + maxlen_suffix

    def __repr__(self):
        """
        Магічний метод. Дозволяє отримувати рядкове представлення списку.

        :return: рядкова репрезентація екземпляру.
        """
        initial_queue = tuple(int(i, 16) for i in self.elements[::-1])
        repr_list = str(initial_queue)
        if not self.maxlen:
            return f"CustomQueue{repr_list}"
        else:
            return f"CustomQueue{repr_list[:-1]}, maxlen={self.maxlen})"

    def __add__(self, other):
        """
        Магічний метод. Дозволяє використовувати "+" між екземплярами класу для їх конкатенації.

        :param other: екземпляр CustomQueue який потрібно додати до поточного.
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
        initial_elements = tuple(int(i, 16) for i in self.elements[::-1])
        other_initial_elements = tuple(int(i, 16) for i in other.elements[::-1])
        return CustomQueue(*(other_initial_elements + initial_elements), maxlen=maxlen)

    def __len__(self) -> int:
        """
        Магічний метод. Дозволяє отримувати довжину черги.

        :return: довжина черги.
        """
        return len(self.elements)

    def __getitem__(self, item: Any):
        """
        Магічний метод. Дозволяє діставати значення з колекції по індексу.

        Метод викликає TypeError при спробі індексування,
        оскільки черги не передбачають такої можливості.
        :param item: індекс.
        :raise TypeError: при спробі отримання елемента за індексом.
        """
        raise TypeError("'CustomQueue object' object is not subscriptable")

    def __iter__(self) -> CustomQueue:
        """
        Магічний метод. Створює об'єкт ітератор.

        :return: ітератор.
        """
        self.n = self.__len__() - 1
        return self

    def __next__(self) -> str:
        """
        Повертає наступний елемент у черзі.

        :return: значення з черги.
        :raises StopIteration: при завершенні ітерації.
        """
        try:
            result = self.elements[self.n]
        except IndexError:
            raise StopIteration
        else:
            self.n -= 1
            return result

    @staticmethod
    def _validate_hex(hex_value):
        """
        Валідує значення hex.

        :param hex_value: хекс.
        :raises ValueError: якщо хекс невалідний.
        """
        try:
            int(hex_value, 16)
        except ValueError:
            raise ValueError(
                "queue can contain only hex values.{} is incorrect value.".format(hex_value)
            )


def custom_queue(
    elements: Sequence[int], maxlen: int = 0, auto_maxlen: bool = False
) -> CustomQueue:
    """
    Конструктор CustomQueue. Конвертує ітерабельний об'єкт в CustomQueue.

    :param elements: об'єкт який потрібно конвертувати в CustomQueue.
    :param maxlen: необов'язковий параметр.
        Дозволяє встановити максимальну довжину черги.
        Якщо дорівнює 0 то кількість елементів необмежена.
    :param auto_maxlen: якщо дорівнює True то maxlen CustomQueue'а
        буде дорівнювати довжині об'єкту, що конвертується.
    :return: CustomQueue сформований з ітерабельного об'єкту.
    """
    if auto_maxlen:
        maxlen = len(elements)
    return CustomQueue(*elements, maxlen=maxlen)
