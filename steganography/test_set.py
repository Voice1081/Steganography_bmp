import unittest
from pack import Package
from unpack import Unpacking


class TestSteganography(unittest.TestCase):

    def setUp(self):
        self.container_without_palette_name = 'container.bmp'
        self.container_with_palette_name = 'test1.bmp'
        self.message_text_name = ['message_text.txt']
        self.little_text_name = ['little_text.txt']
        self.message_image_name = ['message_image.bmp']
        with open(self.message_text_name[0], 'rb') as f:
            self.message_text = f.read()
        with open(self.message_image_name[0], 'rb') as f:
            self.message_image = f.read()
        with open(self.little_text_name[0], 'rb') as f:
            self.little_text = f.read()
        self.several_files = [self.message_text, self.message_image]
        self.several_files_names = [self.message_text_name[0],
                                    self.message_image_name[0]]

    def test_text(self):
        package = Package(self.container_without_palette_name,
                          self.message_text_name)
        package.hide()
        unpack = Unpacking(self.container_without_palette_name)
        result = unpack.extract()
        self.assertEqual(result[0][0][0], self.message_text)
        self.assertEqual(result[1][0], self.message_text_name[0])

    def test_image(self):
        package = Package(self.container_without_palette_name,
                          self.message_image_name)
        package.hide()
        unpack = Unpacking(self.container_without_palette_name)
        result = unpack.extract()
        self.assertEqual(result[0][0][0], self.message_image)
        self.assertEqual(result[1][0], self.message_image_name[0])

    def test_several_files(self):
        package = Package(self.container_without_palette_name,
                          self.several_files_names)
        package.hide()
        unpack = Unpacking(self.container_without_palette_name)
        result = unpack.extract()
        for i in range(2):
            self.assertEqual(result[0][i][0], self.several_files[i])
            self.assertEqual(result[1][i], self.several_files_names[i])

    def test_with_palette(self):
        package = Package(self.container_with_palette_name,
                          self.little_text_name)
        package.hide()
        unpack = Unpacking(self.container_with_palette_name)
        result = unpack.extract()
        self.assertEqual(result[0][0][0], self.little_text)
        self.assertEqual(result[1][0], self.little_text_name[0])

    def test_extract_names(self):
        package = Package(self.container_without_palette_name,
                          self.several_files_names)
        package.hide()
        unpack = Unpacking(self.container_without_palette_name)
        result = unpack.extract_names()
        self.assertEqual(result, self.several_files_names)


if __name__ == '__main__':
    unittest.main()
