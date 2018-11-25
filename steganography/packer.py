import pickle
import zlib
from CRC8 import CRC8


class Packer:
    @staticmethod
    def pack(file_names):
        files = []
        for file_name in file_names:
            with open(file_name, 'rb') as f:
                file = f.read()
                files.append((file, CRC8.get_crc(file)))
        return zlib.compress(pickle.dumps(files))

    @staticmethod
    def unpack(files, names):
        files = pickle.loads(zlib.decompress(files))
        names = pickle.loads(names)
        for i in range(0, len(names)):
            name = names[i]
            file = files[i]
            if file[1] != CRC8.get_crc(file[0]):
                raise Exception('File was changed')
            with open('1' + name, 'wb') as f:
                f.write(file[0])
        return files, names
