class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.nodes = {}

    def add_node(self, value):
        new_node = Node(value)
        self.nodes[value] = new_node
        return new_node

    def connect_nodes(self, value1, value2):
        node1 = self.nodes.get(value1)
        node2 = self.nodes.get(value2)
        if node1 and node2:
            node1.next = node2
            node2.prev = node1

    def create_structure(self):
        for i in range(6):
            self.add_node(i)
            if i > 0:
                self.connect_nodes(i - 1, i)
        
        for i in range(6, 20):
            self.add_node(i)
            self.connect_nodes(i - 1, i)
        self.connect_nodes(19, 0)

        for i in range(20, 25):
            self.add_node(i)
            self.connect_nodes(i - 1, i)
        self.connect_nodes(24, 15)

        for i in range(25, 30):
            self.add_node(i)
            self.connect_nodes(i - 1, i)
        self.nodes[27] = self.nodes[22]
        self.connect_nodes(29, 0)