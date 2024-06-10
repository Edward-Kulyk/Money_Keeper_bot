from abc import ABC, abstractmethod


class IUser(ABC):
    @abstractmethod
    def create_user(self, user_id: str, chat_id: str):
        pass
