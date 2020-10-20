"""Містить реалізацію Хеш-Таблиці."""

from __future__ import annotations
from typing import Tuple, List, Optional, Set, Callable, Iterator, Any
from .utils.typing import IntOrFloat

from .circle import Circle

from math import isclose
from copy import copy


class CircleHashMap:
    """
    Хеш-таблиця з відкритою адресацією.

    Містить в собі об'єкти Circle ключем яких є периметр.
    Хешування відбувається за методом ділення.
    Колізії уникаються методом подвійного хешування.
    """

    def __init__(self, *circles: Circle):
        """
        Ініціалізація хеш-мапи.

        Створює початкові службові колекції та додає у таблицю circles,
        якщо вони передані при ініціалізації.
        :param circles: екземпляри класу Circle.
        """
        self.__real_length_power: int = 1
        self.__keys: Set[IntOrFloat] = set()
        self.__deleted: List[bool] = [False for _ in range(self.__get_real_length())]
        self.__table: List[Optional[Circle]] = [None for _ in range(self.__get_real_length())]
        for circle in circles:
            self.__setitem__(circle.P, circle)

    def items(self) -> List[Tuple[IntOrFloat, Circle]]:
        """
        Дозволяє отримати усі пари ключ-значення з таблиці.

        :return: список з парами ключ-значення.
        """
        result: List[Tuple[IntOrFloat, Circle]] = []
        for key in sorted(self.__keys):
            result.append((key, self.__getitem__(key)))
        return result

    def keys(self) -> List[IntOrFloat]:
        """
        Дозволяє отримати усі ключі з хеш-таблиці.

        :return: список з усім ключами таблиці.
        """
        return sorted(self.__keys)

    def values(self) -> List[Optional[Circle]]:
        """
        Дозволяє отримати ус значення з хеш-таблиці.

        :return: список з усіма значеннями таблиці.
        """
        result = []
        for key in sorted(self.__keys):
            result.append(self.__getitem__(key))
        return result

    def sort_delete(self, func: Callable):
        """
        Видаляє з таблиці усі елементи, з якими func являє True.

        :param func: функція за якою вирішується видаляти елемент чи ні.
        """
        for key in self.keys():
            value = self.__getitem__(key)
            if func(value):
                self.__delitem__(key)

    def __len__(self) -> int:
        """
        Магічний метод. Дозволяє використовувати len().

        :return: кількість ключей у таблиці.
        """
        return len(self.__keys)

    def __get_main_hash(self, key: IntOrFloat) -> int:
        """
        Магічний метод. Отримує хеш методом ділення.

        :param key: ключ хеш якого необхідно отримати.
        :return: Хеш ключа.
        """
        return int(key // self.__get_real_length())

    def __get_fallback_hash(self, key: IntOrFloat) -> int:
        """
        Магічний метод. Отримує допоміжний хеш методом ділення.

        Використовується для запобігання колізій методом подвійного хешування.

        :param key: ключ хеш якого необхідно отримати.
        :return: допоміжний хеш ключа.
        """
        return int(1 + (key // (self.__get_real_length() - 1)))

    def __get_real_length(self) -> int:
        """
        Реальна довжина хеш-таблиці з урахуванням усіх гепів.

        :return: реальна довжина хеш-таблиці.
        """
        return 2 ** self.__real_length_power

    def __resize(self):
        """
        Змінює реальний розмір хеш-таблиці.

        Також перераховує значення хешу тіх елементів, що вже є в таблиці.
        """
        _temporary_table = copy(self.__table)
        self.__real_length_power += 1
        self.__table = [None for _ in range(self.__get_real_length())]
        self.__deleted = [False for _ in range(self.__get_real_length())]
        for circle in _temporary_table:
            if circle is not None:
                h1 = self.__get_main_hash(circle.P)
                h2 = self.__get_fallback_hash(circle.P)
                for shift in range(self.__get_real_length()):
                    if self.__table[h1] is None:
                        self.__table[h1] = circle
                        break
                    h1 = h1 + shift * h2

    def __getitem__(self, key: IntOrFloat) -> Optional[Circle]:
        """
        Магічний метод. Повертає значення ключа з хеш-таблиці.

        :param key: ключ по якому шукається значення.
        :return: значення ключа.
        :raises KeyError: якщо ключа не існує у таблиці.
        """
        h1 = self.__get_main_hash(key)
        h2 = self.__get_fallback_hash(key)
        for shift in range(self.__get_real_length()):
            if self.__table[h1] is not None:
                if isclose(self.__table[h1].P, key) and not self.__deleted[h1]:
                    return self.__table[h1]
            else:
                raise KeyError(key)
            h1 = h1 + shift * h2
        return None

    def __setitem__(
        self, key: IntOrFloat, value: Circle,
    ):
        """
        Магічний метод. Додає пару ключ-значення до таблиці.

        :param key: Ключ.
        :param value: Значення.
        """
        h1 = self.__get_main_hash(key)
        h2 = self.__get_fallback_hash(key)
        for shift in range(self.__get_real_length()):
            try:
                table_value = self.__table[h1]
                deleted_value = self.__deleted[h1]
            except IndexError:
                self.__resize()
                self.__setitem__(key, value)
                return
            if (
                table_value is None
                or deleted_value
                or (table_value is not None and isclose(table_value.P, key))
            ):
                self.__table[h1] = value
                self.__deleted[h1] = False
                self.__keys.add(key)
                break
            h1 = h1 + shift * h2
        else:
            self.__resize()
            self.__setitem__(key, value)

    def __delitem__(self, key: IntOrFloat):
        """
        Магічний метод. Видаляє пару ключ-значення з таблиці.

        :param key: ключ який потрібно видалити.
        """
        h1 = self.__get_main_hash(key)
        h2 = self.__get_fallback_hash(key)
        for shift in range(self.__get_real_length()):
            if self.__table[h1] is not None:
                if isclose(self.__table[h1].P, key):
                    self.__table[h1] = None
                    self.__deleted[h1] = True
                    self.__keys.remove(key)
                    break
            else:
                break
            h1 = h1 + shift * h2

    def __iter__(self) -> Iterator[IntOrFloat]:
        """
        Магічний метод. Робить об'єкт ітерабельним.

        :return: Ітератор з ключами з таблиці.
        """
        yield from self.__keys

    def __contains__(self, item: Any) -> bool:
        """Магічний метод. Перевіряє чи є item у значеннях або ключах таблиці."""
        return item in self.__keys or item in self.__table

    def __repr__(self) -> str:
        """
        Магічний метод. Дозволяє отримувати рядкову репрезентацію таблиці.

        :return: рядкова репрезентація таблиці.
        """
        result = ["CircleHashMap("]
        items = self.values()
        for circle in items[:-1]:
            result.append(repr(circle) + ",")
        result.append(repr(items[-1]))
        result.append(")")
        if self.__len__() <= 8:
            return " ".join(result)
        else:
            return "\n".join(result)

    def __str__(self) -> str:
        """
        Магічний метод. Дозволяє отримувати рядковий варіант таблиці.

        :return: Рядкову таблицю.
        """
        items = self.items()
        result = [f"    {key}: {repr(value)}," for key, value in items[:-1]]
        result.append(f"    {items[-1][0]}: {repr(items[-1][1])}")
        result.insert(0, "{")
        result.append("}")
        return "\n".join(result)
