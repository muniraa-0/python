from abc import ABC, abstractmethod
class absclass(ABC):
    def print(self,x):
        self.print("value:",x)
    @abstractmethod
    def task(self):
        self.print("This is an abstract method")
class test_class(absclass):
    def task(self):
        self.print("This is a sub class")
test_obj = test_class()
test_obj.task()