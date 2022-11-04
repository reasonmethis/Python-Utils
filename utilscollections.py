import json
class AttribDict: #https://databio.org/posts/python_attribute_dict.html
    """
    A class to convert a nested Dictionary into an object with key-values
    accessibly using attribute notation (AttributeDict.attribute) instead of
    key notation (Dict["key"]). This class recursively sets Dicts to objects,
    allowing you to recurse down nested dicts (like: AttributeDict.attr.attr)
    """
    def __init__(self, **entries):
        self.add_entries(**entries)

    def add_entries(self, **entries):
        for key, value in entries.items():
            if type(value) is dict:
                self.__dict__[key] = AttribDict(**value)
            else:
                self.__dict__[key] = value

    def __getitem__(self, key):
        """
        Provides dict-style access to attributes
        """
        return getattr(self, key)

    def __str__(self) -> str:
        return '{' + ', '.join([f'{key} = {repr(value)}' \
            for key, value in self.__dict__.items()]) + '}'

    def dict(self):
        return self.__dict__

    def to_json(self): 
        '''Probably won't work with nested dicts'''
        return json.dumps(self.__dict__)

if __name__ == '__main__':
    st='blah'
    a = AttribDict(x=1, y=st)
    a.z = {'z1': 11, 'z2': 22}
    #del a.dict()['x']
    print(a)