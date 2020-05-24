from os import listdir


class DatabaseGetter:
    def __call__(self, **kwargs):
        file_names = [file for file in listdir('.') if file[-3:].lower() == '.db']
        if len(file_names):
            return file_names[0]
        if kwargs.get('without_exceptions'):
            return False
        raise FileNotFoundError('no db files were found')
