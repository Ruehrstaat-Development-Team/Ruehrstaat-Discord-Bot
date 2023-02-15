class Service:
    def __init__(self, name, label, description, odyssey):
        self.name = name
        self.description = description
        self.label = label
        self.odyssey = odyssey

    def __str__(self):
        return self.label

    def getName(self):
        return self.name

    def getLabel(self):
        return self.label

    def getDescription(self):
        return self.description

    def getOdyssey(self):
        return self.odyssey
