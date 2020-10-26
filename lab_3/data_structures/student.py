"""Містить реалізацію класу студента."""

from __future__ import annotations

__all__ = ["Student"]


class Student:
    """Простий клас контейнер. Зберігає інформацію про студента."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        course: int,
        ticket: int,
        sex: str,
        average_grade: str,
    ):
        """
        Ініціалізація класу. Встановлення атрибутів.

        :param first_name: Ім'я
        :param last_name: Прізвище
        :param course: Курс
        :param ticket: Студентський квиток
        :param sex: Стать
        :param average_grade: Середній бал
        """
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.course: int = course
        self.ticket: int = ticket
        self.sex: str = sex
        self.average_grade: str = average_grade

    def __lt__(self, other: object) -> bool:
        """Менше."""
        if not isinstance(other, self.__class__):
            raise TypeError(
                "you can compare Student only with other Student (not {})".format(
                    type(other).__name__
                )
            )
        return self.ticket < other.ticket

    def __le__(self, other: object) -> bool:
        """Меше або дорінює."""
        if not isinstance(other, self.__class__):
            raise TypeError(
                "you can compare Student only with other Student (not {})".format(
                    type(other).__name__
                )
            )
        return self.ticket <= other.ticket

    def __eq__(self, other: object) -> bool:
        """Дорівнює."""
        if not isinstance(other, self.__class__):
            raise TypeError(
                "you can compare Student only with other Student (not {})".format(
                    type(other).__name__
                )
            )
        return self.ticket == other.ticket

    def __ge__(self, other: object) -> bool:
        """Більше або дорівнює."""
        if not isinstance(other, self.__class__):
            raise TypeError(
                "you can compare Student only with other Student (not {})".format(
                    type(other).__name__
                )
            )
        return self.ticket >= other.ticket

    def __gt__(self, other: object) -> bool:
        """Більше."""
        if not isinstance(other, self.__class__):
            raise TypeError(
                "you can compare Student only with other Student (not {})".format(
                    type(other).__name__
                )
            )
        return self.ticket > other.ticket

    def __repr__(self) -> str:
        """
        Магічний метод. Дозволяє отримувати репрезентацію класу.

        :return: рядкова репрезентація класу.
        """
        return (
            f"Student("
            f"first_name={self.first_name},"
            f"last_name={self.last_name},"
            f"course={self.course},"
            f"ticket={self.ticket},"
            f"sex={self.sex},"
            f"average_grade={self.average_grade})"
        )

    def __str__(self) -> str:
        """
        Магічний метод. Дозволяє отримувати рядкове представлення класу.

        :return: рядкове представлення класу.
        """
        return f"Студент {self.ticket}"
