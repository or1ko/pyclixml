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

if __name__ == "__main__":
    unittest.main()