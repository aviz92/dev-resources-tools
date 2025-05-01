# dataclass_namedtuple_typedict.py

# 📌 Principle:
# DataClass: A @dataclass automatically generates special methods for classes, like __init__, __repr__, and __eq__. It’s used to store data in an organized way, and is mutable.
# NamedTuple: A NamedTuple is an immutable object that defines fields using names, which can be accessed like attributes. It’s lightweight compared to a full class, but it is immutable once created.
# TypedDict: A TypedDict allows for creating a dictionary with a specific set of keys and value types. It is used to define structured dictionaries, providing type safety.
# These structures are useful in different situations, depending on whether you need immutability (NamedTuple), automatic method generation (DataClass), or a dictionary with specific fields (TypedDict).

from dataclasses import dataclass
from typing import NamedTuple, TypedDict


# 1. DataClass
@dataclass
class PersonDataClass:
    first_name: str
    last_name: str
    age: int


# 2. NamedTuple
class PersonNamedTuple(NamedTuple):
    first_name: str
    last_name: str
    age: int


# 3. TypedDict
class PersonTypedDict(TypedDict):
    first_name: str
    last_name: str
    age: int


def main():
    # Using DataClass
    person_dc = PersonDataClass("John", "Doe", 30)
    print("DataClass:", person_dc)

    # Using NamedTuple
    person_nt = PersonNamedTuple("Jane", "Doe", 25)
    print("NamedTuple:", person_nt)

    # Using TypedDict
    person_td: PersonTypedDict = {"first_name": "Alice", "last_name": "Smith", "age": 28}
    print("TypedDict:", person_td)


if __name__ == "__main__":
    main()
