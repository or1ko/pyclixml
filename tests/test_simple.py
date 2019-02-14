# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
import pyclixml as cli
import xml.etree.ElementTree as ET
import unittest

class TestCliXmlParser(unittest.TestCase):
    def test_string(self):
        exampleXml = """
        <S xmlns="http://schemas.microsoft.com/powershell/2004/04">This is String</S>
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertEqual("This is String", ret)
    
    def test_character(self):
        exampleXml = """
        <C xmlns="http://schemas.microsoft.com/powershell/2004/04">97</C>
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertEqual("a", ret)

    def test_unicode_character(self):
        exampleXml = """
        <C xmlns="http://schemas.microsoft.com/powershell/2004/04">12354</C>
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertEqual("あ", ret)

    def test_boolean_true(self):
        exampleXml = """
        <B xmlns="http://schemas.microsoft.com/powershell/2004/04">true</B>
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertTrue(ret)

    def test_boolean_false(self):
        exampleXml = """
        <B xmlns="http://schemas.microsoft.com/powershell/2004/04">false</B>
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertFalse(ret)

    def test_Date_Time(self):
        exampleXml = """
        <DT xmlns="http://schemas.microsoft.com/powershell/2004/04">2019-02-14T21:44:13.419689+09:00</DT>
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertEqual(ret.year, 2019)
        self.assertEqual(ret.month, 2)
        self.assertEqual(ret.day, 14)
        self.assertEqual(ret.hour, 21)
        self.assertEqual(ret.minute, 44)
        self.assertEqual(ret.second, 13)

if __name__ == "__main__":
    unittest.main()