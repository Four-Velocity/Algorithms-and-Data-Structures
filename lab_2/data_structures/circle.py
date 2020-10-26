"""Містить реалізацію Кола."""

from __future__ import annotations
from math import pi, isclose
from typing import Any
from .utils.typing import IntOrFloat

__all__ = ["Circle"]


class Circle:
    """
    Мінімальна реалізація Кола.

    Зберігає координати вершини та радіус кола.
    Також через property реалізовані атрибути периметру та площі.
    """

    def __init__(self, x: IntOrFloat, y: IntOrFloat, r: IntOrFloat):
        """
        Конструктор кола.

        Зберігає координати вершини та радіус кола в атрибути класу.
        :param x: координата центра X
        :param y: координата центра Y
        :param r: радіус кола
        :raises ValueError: якщо радіус є негативним.
        """
        if r < 0:
            raise ValueError("radius can't be negative")
        self.x = x
        self.y = y
        self.r = r

    @property
    def P(self) -> float:
        """
        Периметр кола.

        Викликає приватний метод класу для обрахунку периметра.
        Атрибут периметр обгорнуто в property для того,
        щоб обмежити його модифікацію користувачем.

        :return: периметр кола
        """
        return round(self.__perimeter(), 3)

    @P.setter
    def P(self, value: Any):
        """
        Setter атрибуту P.

        Забороняє змінювати периметр вручну.

        :param value: ...
        :raise AttributeError: при спробі змінити периметр.
        """
        raise AttributeError("you can' change circle's perimeter")

    @P.deleter
    def P(self):
        """
        Deleter атрибуту P.

        Забороняє видаляти периметр.

        :raise AttributeError: при спробі видалити периметр.
        """
        raise AttributeError("you can't delete circle's perimeter")

    @property
    def A(self) -> float:
        """
        Площа кола.

        Викликає приватний метод класу для обрахунку площі.
        Атрибут площі обгорнуто в property для того,
        щоб обмежити його модифікацію користувачем.

        :return: площа кола
        """
        return round(self.__area(), 3)

    @A.setter
    def A(self, value: Any):
        """
        Setter атрибуту A.

        Забороняє змінювати площу вручну.

        :param value: ...
        :raise AttributeError: при спробі змінити площу.
        """
        raise AttributeError("you can' change circle's area")

    @A.deleter
    def A(self):
        """
        Deleter атрибуту A.

        Забороняє видаляти площу.

        :raise AttributeError: при спробі видалити площу.
        """
        raise AttributeError("you can't delete circle's area")

    def __perimeter(self) -> float:
        """Обчислює периметр кола."""
        return 2 * pi * self.r

    def __area(self) -> float:
        """Обчислює площу кола."""
        return pi * (self.r ** 2)

    def __repr__(self) -> str:
        """
        Магічний метод. Дозволяє отримувати рядкове представлення кола.

        :return: рядкова репрезентація кола.
        """
        return f"Circle(x={self.x}, y={self.y}, r={self.r})"

    def __str__(self) -> str:
        """
        Магічний метод. Дозволяє отримати лексичний опис кола.

        :return: лексична версія об'єкту.
        """
        description = f"""\
Circle:
    Coordinates: {self.x}:{self.y}
         Radius: {self.r}
      Perimeter: {self.P}
           Area: {self.A}\
"""
        return description

    def __eq__(self, other: Any) -> bool:
        """Магічний метод. Реалізує порівняння об'єктів між собою."""
        if isinstance(other, self.__class__):
            return (
                isclose(self.P, other.P) and isclose(self.x, other.x) and isclose(self.y, other.y)
            )
        else:
            return False

    def __division_hash__(self, length: int) -> int:
        """
        Магічний метод. Отримує хеш кола методом ділення.

        :param length: довжина хеш-таблиці.
        :return: Хеш кола.
        """
        return int(self.P // length)

    def __helped_hash__(self, length: int) -> int:
        """
        Магічний метод. Отримує допоміжний хеш методом ділення.

        Використовується для запобігання колізій методом подвійного хешування.

        :param length: довжина хеш-таблиці.
        :return: Допоміжний хеш кола.
        """
        return int((self.P // (length - 1)) + 1)
