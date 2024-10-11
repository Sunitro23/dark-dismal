class ErrorChecker:
    def __init__(self, *elements: "ValidationElement") -> None:
        self.elements = elements

    @property
    def no_errors(self) -> bool:
        return all(validation(element.value) for element in self.elements for validation in element.validation.values())
