import json

class Domain:
    state: dict
    startedSubclasses: list[str]
    subclassOrder: list[str]

    def __init__(self, state: dict = None, startedSubclasses: list[str] = None, subclassOrder: list[str] = None):
        self.state = state if state is not None else {}
        self.startedSubclasses = startedSubclasses if startedSubclasses is not None else []
        self.subclassOrder = subclassOrder if subclassOrder is not None else [
            "diver",
            "gear",
            "environment",
            "plan",
        ]

    def getFact(self, name: str) -> str:
        """
        Retrieves the value of a fact in the domain.
        """
        return self.state.get(name, None)
    
    def setFact(self, name: str, value: str) -> None:
        """
        Sets a fact within the domain to the given value.
        """
        self.state[name] = value
    
    def getCurrentSubclass(self) -> str | None:
        try:
            return self.startedSubclasses[-1]
        except IndexError:
            return None
    
    def startSubclass(self, name: str) -> bool:
        """
        Should be called every time a subclass gets used.
        Will return True or False to indicate whether the subclass was already started.
        """
        if name not in self.startedSubclasses:
            self.startedSubclasses.append(name)
            return True
        return False
    
    def completeSubclass(self, name: str) -> bool:
        """
        Should be called every time a subclass is completed.
        Will return True or False to indicate whether the subclass was already completed.
        """
        if name in self.subclassOrder:
            self.subclassOrder.remove(name)
            return True
        return False

    def toJson(self) -> str:
        """
        Converts the Domain instance to a json object.
        """
        return json.dumps({
            "state": self.state,
            "startedSubclasses": self.startedSubclasses,
            "subclassOrder": self.subclassOrder,
        })
    
    @staticmethod
    def fromJson(s: str):
        """
        Initializes a Domain instance from the provided json string.
        Should only be called with json strings produced by Domain.toJson.
        """
        obj: dict = json.loads(s)
        return Domain(
            state=obj["state"],
            startedSubclasses=obj["startedSubclasses"],
            subclassOrder=obj["subclassOrder"]
        )
