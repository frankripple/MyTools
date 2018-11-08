import unittest
import tools
import os

class TestTools(unittest.TestCase):
    def is_txt_file(self,file_name):
        if file_name.split('.')[-1] == 'txt':
            return True
        else:
            return False
    
    def test_find_file(self):
        '''
        Test for all conditions of findallfilesbyname and findallfilesbyCondition
        '''
        current_patch = os.path.abspath('.')
        test_path = 'ut'
        r = tools.findallfilesbyname(test_path,'UT1')
        expected = [os.path.join(current_patch,test_path,'ForUT1.txt'),]
        self.assertEqual(r,expected)

        r = tools.findallfilesbyname(test_path)
        expected = [os.path.join(current_patch,test_path,'ForUT1.txt'),
        os.path.join(current_patch,test_path,'ForUT2.txt'),
        ]
        self.assertEqual(r,expected)

        r = tools.findallfilesbyname(test_path,'NonExistFile')
        self.assertEqual(r,[])

        with self.assertRaises(NotADirectoryError):
            tools.findallfilesbyname('NonExistPath','NonExistFile')

        with self.assertRaises(NotADirectoryError):
            tools.findallfilesbyname('ut\\ForUT1.txt','NonExistFile')

        with self.assertRaises(NotADirectoryError):
            tools.findallfilesbyCondition('NonExistPath',self.is_txt_file)

        r = tools.findallfilesbyCondition(test_path,self.is_txt_file)
        expected = [os.path.join(current_patch,test_path,'ForUT1.txt'),
        os.path.join(current_patch,test_path,'ForUT2.txt'),
        ]
        self.assertEqual(r,expected)
    
    def test_get_time(self):
        '''
        Test for get time tools
        '''
        self.assertEqual(tools.get_current_time('%123'),'Error Time Format')


if __name__ == '__main__':
    unittest.main()