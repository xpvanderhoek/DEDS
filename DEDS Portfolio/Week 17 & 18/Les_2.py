from abc import ABC, abstractmethod

class LinkedList(ABC):
    @abstractmethod
    def addFirst(self, getal):
        pass

    @abstractmethod
    def removeAll(self, value):
        pass

    @abstractmethod
    def remove(self, value):
        pass
    @abstractmethod
    def greatest(self, value):
        pass

    @abstractmethod
    def toString(self):
        pass

    @abstractmethod
    def isEmpty(self):
        pass

    @abstractmethod
    def uniq(self):
        pass

    @abstractmethod
    def sortSimple(self):
        pass

    @abstractmethod
    def pickFirst(self):
        pass

class LinkedListPopulated(LinkedList):
    def __init__(self, getal, volgendeObject):
        self.getal = getal
        self.volgendeObject = volgendeObject

    def isEmpty(self):
        return False
    def addFirst(self, getal):
        return LinkedListPopulated(getal, self)

    def remove(self, value):
        if self.getal == value:
            return self.volgendeObject
        else:
            nieuweVolgende = self.volgendeObject.remove(value)
            return LinkedListPopulated(self.getal, nieuweVolgende)

    def removeAll(self, value):
        if self.getal == value:
            return self.volgendeObject.removeAll(value)
        else:
            nieuweVolgende = self.volgendeObject.removeAll(value)
            return LinkedListPopulated(self.getal, nieuweVolgende)

    def greatest(self, value):
        if self.getal > value:
            value = self.getal
        return self.volgendeObject.greatest(value)

    def sortSimple(self):
        lijst = self
        gesorteerdeLijst = LinkedListEmpty()
        while not lijst.isEmpty():
            grootste = lijst.greatest(0)
            gesorteerdeLijst = gesorteerdeLijst.addFirst(grootste)
            lijst = lijst.remove(grootste)
        return gesorteerdeLijst

    def uniq(self):
        lijst = self
        unique = 0
        while not lijst.isEmpty():
            getal = lijst.pickFirst()
            unique += 1
            lijst = lijst.removeAll(getal)
        return unique

    def pickFirst(self):
        return self.getal

    def toString(self):
        return str(self.getal) + " " + self.volgendeObject.toString()

class LinkedListEmpty(LinkedList):
    def addFirst(self, getal):
        return LinkedListPopulated(getal, self)
    def isEmpty(self):
        return True
    def toString(self):
        return ""
    def removeAll(self, value):
        return self
    def remove(self, value):
        return self
    def greatest(self, value):
        return value
    def sortSimple(self):
        return self

    def uniq(self):
        return self
    def pickFirst(self):
        return self


lijst = LinkedListEmpty()
lijst = lijst.addFirst(7)
lijst = lijst.addFirst(4)
lijst = lijst.addFirst(5)
lijst = lijst.addFirst(4)
gesorteerd = lijst.uniq()
print(gesorteerd)

