import random

class DSU (object):
    def __init__(self):
        self.dsu = {}
        self.count = 0

    def make(self, node):
         self.dsu[node] = node
         self.count += 1

    def add(self, node, parent):
        self.dsu[node] = parent

    def find(self, node):
        if self.dsu[node] = node:
            return node
        else
            return self.find(self.dsu[node])

    def join(self, node1, node2):
        head1 = self.find(node1)
        head2 = self.find(node2)

        if head1 == head2:
            return head1
        
        if random.randint(0,1):
            tmp = head1
            head1 = head2
            head2 = tmp

        self.dsu[head2] = head1
        self.count -= 1
        
        return head1

            

        
        
        
