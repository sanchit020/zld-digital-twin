from abc import ABC, abstractmethod


class Asset(ABC):

    @abstractmethod
    def update(self, state, dt):
        raise NotImplementedError(
            "Every asset must implement update(state, dt)."
        )