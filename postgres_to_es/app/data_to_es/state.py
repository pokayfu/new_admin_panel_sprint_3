from typing import Any, Dict
import json
import os


class JsonFileStorage:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def save_state(self, state: Dict[str, Any]):
        storage_data = self.retreive_state()
        with open(self.file_path, 'w') as f:
            f.write(json.dumps({**storage_data,  **state}))

    def retreive_state(self):
        if not os.path.exists(self.file_path):
            os.mknod(self.file_path)
            return {}
        with open(self.file_path, 'r') as f:
            storage_data = f.read()
            if not storage_data:
                return {}
            return json.loads(storage_data)


class State:
    def __init__(self, storage) -> None:
        self.storage = storage

    def set_state(self, key: str, value: Any):
        self.storage.save_state({key: value})

    def get_state(self, key: str):
        storage_data = self.storage.retreive_state()
        return storage_data.get(key)
    