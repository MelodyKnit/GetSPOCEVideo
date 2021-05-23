from logging import info, error, INFO, basicConfig


class Logger:
    basicConfig(level=INFO, format='\033[38;5;255m%(asctime)s %(message)s\033[m')

    @staticmethod
    def download(msg: str):
        info("\033[33m[DOWNLOAD]: " + msg + "\033[m")

    @staticmethod
    def timeout(msg: str):
        error("\033[31m[TIMEOUT]: " + msg + "\033[m")

    @staticmethod
    def completed(msg: str):
        info("\033[32m[COMPLETED]: " + msg + "\033[m")


__all__ = [
    "Logger"
]
