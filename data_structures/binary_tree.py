"""Містить реалізацію простого бінарного дерева."""

from __future__ import annotations
from typing import Optional, Callable, Tuple, Iterator, List
from .student import Student
from collections import deque
from rich.console import Console


class Node:
    """Вузол бінарного дерева."""

    def __init__(self, value: Student, left: Optional[Node] = None, right: Optional[Node] = None):
        """
        Ініціалізація вузла.

        :param value: значення вузла.
        :param left: дочірній елемент ліворуч.
        :param right: дочірній елемент праворуч.
        """
        self.v = value
        self.l = left  # noqa
        self.r = right  # noqa

    def display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.r is None and self.l is None:
            line = '%s' % self.v.ticket
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.r is None:
            lines, n, p, x = self.l.display_aux()
            s = '%s' % self.v.ticket
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.l is None:
            lines, n, p, x = self.r.display_aux()
            s = '%s' % self.v.ticket
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.l.display_aux()
        right, m, q, y = self.r.display_aux()
        s = '%s' % self.v.ticket
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


class Tree:
    """Реалізація простого дерева. Дерево підтримує вставки, пошук та видалення."""

    def __init__(self):
        """Ініціалізує атрибут екземпляру root."""
        self.root = None

    def add(self, val: Student):
        """
        Додає значення у дерево.

        :param val: значення яке потрібно додати.
        """
        if self.root is None:
            self.root = Node(val)
        else:
            self._add(val, self.root)

    def _add(self, val: Student, node: Node):
        """
        Рекурсивна функція. Додає значення в найбільш підходяще місце у дереві.

        :param val: значення яке потрібно додати у дерево.
        :param node: вузол, діти якого перевіряються на вільність.
        """
        if val < node.v:
            if node.l is not None:
                self._add(val, node.l)
            else:
                node.l = Node(val)  # noqa
        else:
            if node.r is not None:
                self._add(val, node.r)
            else:
                node.r = Node(val)  # noqa

    def findall_lazy(self, key: Callable) -> Iterator[Tuple[Node, int]]:
        """
        Знаходить всі значення, з якими key повертає True.

        :param key: функція-фільтр.
        :return: ітератор з вузлами та їх рівнями вкладеності у дереві.
        """
        for node, level in self:
            if key(node.v):
                yield node, level

    def findall(self, key: Callable) -> List[Tuple[Node, int]]:
        """
        Знаходить всі значення, з якими key повертає True та упаковує їх у список.

        :param key: функція-фільтр.
        :return: список з усіма значеннями, що відповідають критеріям.
        """
        return [(node, level) for node, level in self.findall_lazy(key)]

    @staticmethod
    def __find_min(node: Node) -> Node:
        """Знаходить вузол з найменшим значенням у гілці."""
        current = node

        while current.l is not None:
            current = current.l

        return current

    def delete_all(self, key: Callable):
        """
        Видаляє з дерева усі об'єкти, що відповідають критеріям key.

        :param key: функція-фільтр.
        """
        for_delete_list = self.findall(key)
        for_delete_list.sort(key=lambda x: x[1], reverse=True)
        for node, _ in for_delete_list:
            self.delete_node(self.root, node.v)

    def delete_node(self, root: Optional[Node], key: Student):
        """
        Рекурсивна функція. Видаляє вузол з дерева.

        Працює вне залежності від кількості дитячих вузлів.

        :param root: вузол, з якого починається видалення.
        :param key: значення вузла яке потрібно видалити
        :return: вузол.
        """
        if root is None:
            return root

        if key < root.v:
            root.l = self.delete_node(root.l, key)  # noqa
        elif key > root.v:
            root.r = self.delete_node(root.r, key)
        else:
            if root.l is None:
                temp = root.r
                root = None
                return temp
            elif root.r is None:
                temp = root.l
                root = None
                return temp

            temp = self.__find_min(root.r)

            root.v = temp.v
            root.r = self.delete_node(root.r, temp.v)

        return root

    def __iter__(self):
        """
        Магічний метод.

        Разом із __next__ реалізують можливість ітеруватись по дереву у ширину.
        """
        self.queue = deque()
        self.queue.append((self.root, 0))
        return self

    def __next__(self):
        """
        Магічнйи метод.

        Разом із __iter__ реалізують можливість ітеруватись по дереву у ширину.
        """
        if len(self.queue):
            node, lvl = self.queue.popleft()
            if node.l is not None:
                self.queue.append((node.l, lvl + 1))
            if node.r is not None:
                self.queue.append((node.r, lvl + 1))
            return node, lvl
        raise StopIteration

    def __str__(self):
        lines, *_ = self.root.display_aux()
        for line in lines:
            print(line)
