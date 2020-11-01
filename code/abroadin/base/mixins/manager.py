class GetListManagerMixin:
    def list(self):
        return [obj for obj in self._chain()]