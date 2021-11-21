class Node:
    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next


class DoubleLinkedList:
    def __init__(self, data):
        node = Node(data)
        self.head = node
        self.tail = node

    def add_node(self, data, prev, next):
        node = Node(data, prev, next)
        if prev is not None and next is not None:
            prev.next = node
            next.prev = node
        elif prev is None and next == self.head:
            self.head.prev = node
            self.head = node
        elif prev == self.tail and next is None:
            self.tail.next = node
            self.tail = node
        elif prev is None and next is None:
            self.head = node
            self.tail = node

    def remove_node(self, node):
        if node.prev is not None:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        del node

    def is_in(self, data):
        c = self.head
        while c is not None and c.data != data:
            c = c.next
        return c is not None

    def find(self, data):
        c = self.head
        while c is not None and c.data != data:
            c = c.next
        return c

    def is_empty(self):
        return self.head is None and self.tail is None


if __name__ == "__main__":
    l = DoubleLinkedList(3)
    current = l.head
    l.add_node(2, next=current, prev=None)
    l.add_node(4, prev=current, next=None)
    l.add_node(6, prev=current.next, next=None)
    l.add_node(5, prev=current.next, next=current.next.next)

    print(l.is_in(2))
    print(l.is_in(6))
    print(l.is_in(5))
    print(l.is_in(7))

    print(l.find(3).data)
    print(l.find(2).data)
    print(l.find(6).data)


    l.remove_node(l.head)
    l.remove_node(l.tail)
    l.remove_node(current.next)
    l.remove_node(l.head)
    l.remove_node(l.tail)

    print("bla")