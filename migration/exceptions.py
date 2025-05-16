class DuplicateDataError(Exception):
    def __init__(self, message, duplicates, entity):
        super().__init__()
        self.message = message
        self.duplicates = duplicates
        self.entity = entity


class InvalidModelError(Exception):
    pass


class EmptyDataFrameError(Exception):
    pass


class EmptyAvroFile(Exception):
    pass


class IncompatibleAvroFileError(Exception):
    def __init__(self, message):
        self.message = message
