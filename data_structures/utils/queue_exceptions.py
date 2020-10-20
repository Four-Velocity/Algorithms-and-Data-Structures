"""Містить кастомні помилки для data_structures.queue.CustomQueue."""

__all__ = ["CustomQueueIsFull", "CustomQueueIsEmpty"]


class CustomQueueIsFull(Exception):
    """Черга переповнена."""

    pass


class CustomQueueIsEmpty(Exception):
    """Черга порожня."""

    pass
