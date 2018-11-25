import argparse
from pack import Package
from unpack import Unpacking


def main():
    parser = argparse.ArgumentParser(usage='''
                 You can use this program to pack files into bmp container,
                 extract files from bmp container
                 and extract list of file names
                 Examples:
                 python steganography.py --unpack container.bmp
                 python steganography.py --unpack container.bmp --names
                 python steganography.py --pack container.bmp [FILENAMES]
                 Use flag \'-u\', \'--unpack\' to extract files
                 Use flag \'-p\', \'--pack\' to pack files into container
                 Use flag \'-n\', \'--names\' to get list of filenames
                 Use \'-h\', \'--help\' to read help message
                 ''')
    parser.add_argument('--unpack', '-u', action='store', dest='container',
                        help='extract all files from container')
    parser.add_argument('--names', '-n', action='store_true', default=False,
                        dest='names',
                        help='''extract list of filenames from container
                        Use this flag after --unpack CONTAINERFILENAME''')
    parser.add_argument('--pack', '-p', action='store', nargs='+',
                        dest='container_and_files',
                        help='''pack files in container
                        Write container name and names of files you want to
                        pack into.
                        Pay attention that container file name must be
                        first''')
    args = parser.parse_args()
    if args.container_and_files:
        container = args.container_and_files[0]
        files = args.container_and_files[1:]
        packer = Package(container, files)
        packer.hide()
    if args.container:
        container = args.container
        unpacker = Unpacking(container)
        if args.names:
            names = unpacker.extract_names()
            for name in names:
                print(name)
        else:
            unpacker.extract()


if __name__ == '__main__':
    main()
