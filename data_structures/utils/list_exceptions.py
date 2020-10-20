"""Містить кастомні помилки для data_structures.list.CustomList."""

__all__ = ["CustomListIsFull", "CustomListIsEmpty"]


class CustomListIsFull(Exception):
    """Список повний."""

    pass


class CustomListIsEmpty(Exception):
    """Список порожній."""

    pass
