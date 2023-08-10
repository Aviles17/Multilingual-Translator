class NotSupportedLan(Exception):
    def __init__(self, lan: str):
        self.message = f"Sorry, the program doesn't support {lan}"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InternetException(Exception):
    def __str__(self):
        return "Something wrong with your internet connection"


class WordNotFound(Exception):
    def __init__(self, word: str):
        self.message = f"Sorry, unable to find {word}"
        super().__init__(self.message)

    def __str__(self):
        return self.message