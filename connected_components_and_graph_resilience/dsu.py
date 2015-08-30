import random

class DSU (object):
    """ disjoint set union data structure """
    
    def __init__(self):
        """ init """
        self._dsu = {}
        self._head = {}
        self._count = 0

    def cmax(self, cnt):
        """ check max count """
        if self._count < cnt:
            self._count = cnt

    def count(self):
        """ count set connected components """
        return self._count

    def make(self, node):
        """ set head """
        self._dsu[node] = node
        self._head[node] = 1
        self.cmax(self._head[node])

    def add(self, node, parent):
        """ add node """ 
        self._dsu[node] = parent
        self._head[parent] += 1
        self.cmax(self._head[parent])
          
    def find(self, node):
        """ find head on node """
        if node not in self._dsu:
            return None
        
        return self._find(node)

    def _find(self, node):
        """ find head on node """
        while self._dsu[node] != node:
            node = self._dsu[node]

        return node


    def join(self, node1, node2):
        """ join two cc """
        head1 = self.find(node1)
        head2 = self.find(node2)

        #print 'head1', head1, 'head2', head2, 'dsu', self._dsu 
        
        if head1 == head2:
            return head1
        
        if random.randint(0,1):
            head1, head2 = head2, head1


        self._dsu[head2] = head1
        self._head[head1] += self._head[head2]
        del self._head[head2]
        self.cmax(self._head[head1])
        
        return head1

            

        
        
        
