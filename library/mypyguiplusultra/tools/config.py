from pathlib import Path
import json

class Config:
    def __init__(self, path : str):
        self.file = Path(path)
        if not self.file.is_file():raise FileNotFoundError('Config path is invalid')
        self.conf = json.loads(self.file.read_text())

    def __enter__(self):
        return self.conf

    def __exit__(self, *args):
        self.file.write_text(json.dumps(self.conf, indent=4))
