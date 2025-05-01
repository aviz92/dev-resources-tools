# observer_pattern.py

# 📌 Principle:
# The Observer Pattern (also known as PubSub) allows a subject to notify a list of observers when a change occurs. In this example:
# Observer is the abstract class, and ConcreteObserverA and ConcreteObserverB are concrete observers.
# Subject maintains a list of observers and notifies them when something changes.
# The notify method allows the subject to send a message to all registered observers.
# This pattern is particularly useful when one object needs to update multiple other objects in response to a change (e.g., UI updates, event handling).

from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass


class ConcreteObserverA(Observer):
    def update(self, message: str):
        print(f"ConcreteObserverA received: {message}")


class ConcreteObserverB(Observer):
    def update(self, message: str):
        print(f"ConcreteObserverB received: {message}")


class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)


def main():
    # Create the subject and observers
    subject = Subject()
    observer_a = ConcreteObserverA()
    observer_b = ConcreteObserverB()

    # Attach observers to the subject
    subject.attach(observer_a)
    subject.attach(observer_b)

    # Notify all observers
    subject.notify("New message!")

    # Detach an observer and notify again
    subject.detach(observer_b)
    subject.notify("Another message!")


if __name__ == "__main__":
    main()
