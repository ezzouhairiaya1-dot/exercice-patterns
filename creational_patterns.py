"""Creational patterns: they control how objects are created.

1. Singleton       : only one instance of a class exists
2. Factory Method  : a superclass defines the creation, subclasses choose the type
3. Builder         : build a complex object step by step
"""

from abc import ABC, abstractmethod


# ====================================================================
# 1. SINGLETON
# Problem: one shared configuration for the whole app.
# Idea: __new__ always returns the same object.
# ====================================================================
class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.settings = {"language": "en", "debug": False}
        return cls._instance


# ====================================================================
# 2. FACTORY METHOD
# Problem: the app sends notifications, but the type (email, SMS) changes.
# Idea: the creator calls an abstract method create_notification();
#       each subclass decides which product to build.
# ====================================================================
class Notification(ABC):              # product interface
    @abstractmethod
    def send(self, message):
        pass


class EmailNotification(Notification):
    def send(self, message):
        return f"Email sent: {message}"


class SMSNotification(Notification):
    def send(self, message):
        return f"SMS sent: {message}"


class NotificationCreator(ABC):       # creator
    @abstractmethod
    def create_notification(self):    # the factory method
        pass

    def notify(self, message):
        # Same code for every type: it does not know the concrete class.
        notification = self.create_notification()
        return notification.send(message)


class EmailCreator(NotificationCreator):
    def create_notification(self):
        return EmailNotification()


class SMSCreator(NotificationCreator):
    def create_notification(self):
        return SMSNotification()


# ====================================================================
# 3. BUILDER
# Problem: a Computer has many optional parts, a huge constructor is ugly.
# Idea: a builder sets the parts one by one; a director knows the recipes.
# ====================================================================
class Computer:                       # the complex product
    def __init__(self):
        self.cpu = None
        self.ram_gb = None
        self.storage_gb = None
        self.gpu = None

    def __str__(self):
        return (f"Computer(cpu={self.cpu}, ram_gb={self.ram_gb}, "
                f"storage_gb={self.storage_gb}, gpu={self.gpu})")


class ComputerBuilder:
    def __init__(self):
        self._computer = Computer()

    def set_cpu(self, cpu):
        self._computer.cpu = cpu
        return self                   # returning self allows chaining

    def set_ram(self, gb):
        self._computer.ram_gb = gb
        return self

    def set_storage(self, gb):
        self._computer.storage_gb = gb
        return self

    def set_gpu(self, gpu):
        self._computer.gpu = gpu
        return self

    def build(self):
        computer = self._computer
        self._computer = Computer()   # reset for the next build
        return computer


class Director:                       # knows the common recipes
    def __init__(self, builder):
        self._builder = builder

    def build_gaming_pc(self):
        return (self._builder.set_cpu("Ryzen 9").set_ram(32)
                .set_storage(2000).set_gpu("RTX 4080").build())

    def build_office_pc(self):
        return (self._builder.set_cpu("Core i3").set_ram(8)
                .set_storage(256).build())


# ====================================================================
# Demo
# ====================================================================
if __name__ == "__main__":
    print("--- Singleton")
    a, b = Config(), Config()
    a.settings["debug"] = True
    print("Same object:", a is b)
    print("Shared state:", b.settings)

    print("\n--- Factory Method")
    for creator in [EmailCreator(), SMSCreator()]:
        print(creator.notify("Your order has shipped"))

    print("\n--- Builder")
    director = Director(ComputerBuilder())
    print(director.build_gaming_pc())
    print(director.build_office_pc())
    custom = ComputerBuilder().set_cpu("M3").set_ram(16).build()
    print(custom)
