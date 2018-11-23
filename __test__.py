'''
Test for tools
'''
import unittest
import os
import tools
def is_txt_file(file_name):
    ''' A function used for tools.findallfilesbyCondition'''
    if file_name.split('.')[-1] == 'txt':
        return True
    return False
class TestTools(unittest.TestCase):
    ''' Test for tools function    '''
    def test_find_file_by_name(self):
        '''
        Test for all conditions of findallfilesbyname
        '''
        current_patch = os.path.abspath('.')
        test_path = 'ut'
        expected = [os.path.join(current_patch, test_path, 'ForUT1.txt'),]
        self.assertEqual(tools.findallfilesbyname(test_path, 'UT1'), expected)

        expected = [
            os.path.join(current_patch, test_path, 'ForUT1.txt'),
            os.path.join(current_patch, test_path, 'ForUT2.txt'),
            os.path.join(current_patch, test_path, 'test.csv'),
        ]
        self.assertEqual(tools.findallfilesbyname(test_path), expected)

        self.assertEqual(tools.findallfilesbyname(test_path, 'NonExistFile'), [])

        with self.assertRaises(NotADirectoryError):
            tools.findallfilesbyname('NonExistPath', 'NonExistFile')

        with self.assertRaises(NotADirectoryError):
            tools.findallfilesbyname('ut\\ForUT1.txt', 'NonExistFile')

    def test_find_file_by_condition(self):
        '''
        Test for all conditions findallfilesbyCondition
        '''
        current_patch = os.path.abspath('.')
        test_path = 'ut'
        with self.assertRaises(NotADirectoryError):
            tools.findallfilesbycondition('NonExistPath', is_txt_file)

        expected = [
            os.path.join(current_patch, test_path, 'ForUT1.txt'),
            os.path.join(current_patch, test_path, 'ForUT2.txt'),
        ]
        self.assertEqual(tools.findallfilesbycondition(test_path, is_txt_file), expected)

    def test_get_time(self):
        ''' Test for get time tools '''
        self.assertEqual(tools.get_current_time('%123'), 'Error Time Format')

    def test_csv_write_error(self):
        '''Test for csv write function'''
        #Test when file can not be open
        test_file = r'ut\test.csv'
        with self.assertRaises(IOError):
            tools.list_write_to_csv('ut', None)

        with self.assertRaises(TypeError):
            tools.list_write_to_csv(test_file, None)

        content = ['test1', 'test2']
        tools.list_write_to_csv(test_file, content, None)
        with open(test_file) as _f:
            self.assertFalse(_f.read())
        #Can not write funtion because item of content is not list or dict

    def test_csv_write(self):
        '''Test for csv write normal function'''
        content = [['test1', 'test2'],]
        header = ['h1', 'h2', 'h3']
        test_file = r'ut\test.csv'

        tools.list_write_to_csv(test_file, content)
        with open(test_file) as _f:
            self.assertEqual(_f.read(), 'test1,test2\n')

        tools.list_write_to_csv(test_file, content, header)
        with open(test_file) as _f:
            self.assertEqual(_f.read(), 'h1,h2,h3\ntest1,test2\n')

if __name__ == '__main__':
    unittest.main()
