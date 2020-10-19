"""Містить кастомні помилки для data_structures.queue.CustomQueue."""


class CustomQueueIsFull(Exception):
    """Черга переповнена."""

    pass


class CustomQueueIsEmpty(Exception):
    """Черга порожня."""

    pass
