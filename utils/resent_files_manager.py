import json
import os


class ResentFileManager:
    _data_file = 'resent_files.json'

    def __init__(self):
        self.last_file = None
        self.resent_files = []
        self._read_file()

    def _read_file(self):
        filename = os.path.join(os.path.dirname(__file__), ResentFileManager._data_file)
        if not os.path.isfile(filename):
            return

        with open(filename, 'r', encoding='utf8') as file:
            raw_data = file.read()
            data = json.loads(raw_data)
            self.last_file = data['last_file']
            self.resent_files = list(filter(os.path.isfile, data['resent_files']))

    def _update_file(self):
        filename = os.path.join(os.path.dirname(__file__), ResentFileManager._data_file)
        with open(filename, 'w', encoding='utf8') as file:
            data = {'last_file': self.last_file, 'resent_files': self.resent_files}
            file.write(json.dumps(data, indent=4, ensure_ascii=False))

    def add_resent_file(self, file_path):
        self.last_file = file_path
        if file_path in self.resent_files:
            self.resent_files.remove(file_path)

        self.resent_files.append(file_path)
        self._update_file()

    def get_last_file(self):
        return self.last_file

    def get_resent_files(self, max_file_count=10):
        reversed_files = list(reversed(self.resent_files))
        if max_file_count > len(reversed_files):
            return reversed_files[:max_file_count]
        return reversed_files
