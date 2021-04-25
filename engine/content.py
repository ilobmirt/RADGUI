"""================================================================================================
This module is designed to represent a variety of elements in an area.

CLASSES:
    Content
================================================================================================"""
import uuid
from typing import List, Dict, Any
from .Label import Label
from .Column import Column
from .row import Row
from .Button import Button
from .Operator import Operator
from .Property import Property

#==================================================#
#RAD GUI Content Object
#==================================================#

class Content():
    """...
    """
    def __init__(self):
        self._collection: List[List[Any]] = []
        self._namespace: str = ""

    @property
    def namespace(self) -> str:
        """...
        """
        return self._namespace

    @namespace.setter
    def namespace(self,input_value: str) -> None:
        """...
        """
        self._namespace = input_value
        #Update the content of the collection
        for index in self._collection:
            if index[1].__class__.__name__ in ["Column","Row","Operator"]:
                index[1].namespace = self._namespace

    @property
    def value(self) -> List[Dict[str,Any]]:
        """...
        """
        result: List[Dict[str,Any]] = []

        return result

    @value.setter
    def value(self,input_list: List[Dict[str,Any]]) -> None:
        """...
        """
        #Clear the Existing Collection
        self._collection.clear()

        #Add the appropriate object for the new collection
        for index in input_list:
            if "TYPE" not in index:
                continue

            if index["TYPE"] == "LABEL":
                self.add_label(index)

            elif index["TYPE"] == "COLUMN":
                self.add_column(index)

            elif index["TYPE"] == "ROW":
                self.add_row(index)

            elif index["TYPE"] == "BUTTON":
                self.add_button(index)

            elif index["TYPE"] == "OPERATOR":
                self.add_operator(index)

            elif index["TYPE"] == "PROPERTY":
                self.add_property(index)


    def add_label(self,input_attributes: Dict[str,Any], input_index: int = -1) -> str:
        """...
        """
        key_id: str = ""
        new_object = None

        if "TYPE" not in input_attributes:
            return key_id

        if "{}".format(input_attributes["TYPE"]).upper() != "LABEL":
            return key_id

        key_id = uuid.uuid4().hex
        new_object = Label()
        new_object.value = input_attributes

        #Without Input, or if given a negative value, just append to the list
        if input_index < 0:
            input_index = len(self._collection)

        self._collection.insert(input_index,[key_id,new_object])

        return key_id

    def add_column(self,input_attributes: Dict[str,Any], input_index: int = -1) -> str:
        """...
        """
        key_id: str = ""
        new_object = None

        if "TYPE" not in input_attributes:
            return key_id

        if "{}".format(input_attributes["TYPE"]).upper() != "COLUMN":
            return key_id

        key_id = uuid.uuid4().hex
        new_object = Column()
        new_object.namespace = self._namespace
        new_object.value = input_attributes

        #Without Input, or if given a negative value, just append to the list
        if input_index < 0:
            input_index = len(self._collection)

        self._collection.insert(input_index,[key_id,new_object])

        return key_id

    def add_row(self,input_attributes: Dict[str,Any], input_index: int = -1) -> str:
        """...
        """
        key_id: str = ""
        new_object = None

        if "TYPE" not in input_attributes:
            return key_id

        if "{}".format(input_attributes["TYPE"]).upper() != "ROW":
            return key_id

        key_id = uuid.uuid4().hex
        new_object = Row()
        new_object.namespace = self._namespace
        new_object.value = input_attributes

        #Without Input, or if given a negative value, just append to the list
        if input_index < 0:
            input_index = len(self._collection)

        self._collection.insert(input_index,[key_id,new_object])

        return key_id

    def add_button(self,input_attributes: Dict[str,Any], input_index: int = -1) -> str:
        """...
        """
        key_id: str = ""
        new_object = None

        if "TYPE" not in input_attributes:
            return key_id

        if "{}".format(input_attributes["TYPE"]).upper() != "BUTTON":
            return key_id

        key_id = uuid.uuid4().hex
        new_object = Button()
        new_object.value = input_attributes

        #Without Input, or if given a negative value, just append to the list
        if input_index < 0:
            input_index = len(self._collection)

        self._collection.insert(input_index,[key_id,new_object])

        return key_id

    def add_operator(self,input_attributes: Dict[str,Any], input_index: int = -1) -> str:
        """...
        """
        key_id: str = ""
        new_object = None

        if "TYPE" not in input_attributes:
            return key_id

        if "{}".format(input_attributes["TYPE"]).upper() != "OPERATOR":
            return key_id

        key_id = uuid.uuid4().hex
        new_object = Operator()
        new_object.namespace = self._namespace
        new_object.value = input_attributes

        #Without Input, or if given a negative value, just append to the list
        if input_index < 0:
            input_index = len(self._collection)

        self._collection.insert(input_index,[key_id,new_object])

        return key_id

    def add_property(self,input_attributes: Dict[str,Any], input_index: int = -1) -> str:
        """...
        """
        key_id: str = ""
        new_object = None

        if "TYPE" not in input_attributes:
            return key_id

        if "{}".format(input_attributes["TYPE"]).upper() != "PROPERTY":
            return key_id

        key_id = uuid.uuid4().hex
        new_object = Property()
        new_object.value = input_attributes

        #Without Input, or if given a negative value, just append to the list
        if input_index < 0:
            input_index = len(self._collection)

        self._collection.insert(input_index,[key_id,new_object])

        return key_id

    def remove_id(self,target_id: str) -> None:
        """...
        """
        for index in self._collection:
            if target_id == index[0]:
                self._collection.remove(index)
                break

    def __len__(self) -> int:
        """...
        """
        return len(self._collection)

    def length(self) -> int:
        """...
        """
        return len(self)

    def to_code(self, called_by: str = "layout") -> str:
        """...
        """
        result: str = ""
        code_list: List[str] = []

        for index in self._collection:
            code_list.append(index[1].to_code(called_by))

        result = "\n".join(code_list)

        return result
