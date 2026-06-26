from abc import ABC, abstractmethod

class Asset(ABC):

    @abstractmethod
    def update(self, state, dt):
        """
        Update asset state.
        dt in hours.
        """
        pass