class   Message:
    def __init__(self, source, data):
        self.source = source
        self.data = data

class   Channel:
    def __init__(self):
        self.messages = []

    def addMessage(self, source, data):
        self.messages.append(Message(source, data))
        return len(self.messages) - 1

    def getHistory(self):
        return [(i, j.source, j.data) for i, j in enumerate(self.messages)]
