import json
import os
import atexit

# https://stackoverflow.com/questions/16333054/what-are-the-implications-of-registering-an-instance-method-with-atexit-in-pytho
# not efficient, class object lifetime will exist until end of program
# however, we are expecting it to last this long anyway
class MetaDataManager:
    # use dict syntax to directly read from: self.metadata

    def __init__(self, root_dir='.'):
        self.metadata_fn = os.path.join(root_dir, 'api_usage.json')
        if os.path.exists(self.metadata_fn):
            try:
                with open(self.metadata_fn, 'r') as f:
                    self.metadata = json.load(f)
            except Exception as e:
                print('Ignoring MetaDataManager error:', e)
                self.metadata = {}
        else:
            self.metadata = {}
        # automatic cleanup on program exit
        atexit.register(self.save)
    
    def save(self):
        with open(self.metadata_fn, 'w') as f:
            json.dump(self.metadata, f)
            print('MetaDataManager: API usage statistics saved.')

    def increment(self, key, amt=1):
        if key not in self.metadata:
            self.metadata[key] = 0
        self.metadata[key] += amt


if __name__ == '__main__':
    mm = MetaDataManager('..')
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(mm.metadata)