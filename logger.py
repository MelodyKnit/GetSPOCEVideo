from datetime import datetime


class Logger:
    @staticmethod
    def date():
        return str(datetime.today()).split(".")[0]

    @classmethod
    def print(cls, level: str, msg: str):
        print(cls.date(), f"[{level.upper()}]:", msg)

    @classmethod
    def download(cls, msg: str):
        cls.print("download", msg)

    @classmethod
    def timeout(cls, msg: str):
        cls.print("timeout", msg)

    @classmethod
    def completed(cls, msg: str):
        cls.print("completed", msg)

    @classmethod
    def error(cls, msg: str):
        cls.print("error", msg)


__all__ = [
    "Logger"
]
