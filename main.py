import os
from Api.api_class import ApiClass

if __name__ == '__main__':
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Analyzer/files')
    api = ApiClass(folder_path=path)
    api.run()
