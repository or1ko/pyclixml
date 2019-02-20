# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
import pyclixml as cli
import xml.etree.ElementTree as ET
import unittest
import datetime
import uuid
import urllib.parse

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

    def test_duration(self):
        exampleXml = """
        <TS xmlns="http://schemas.microsoft.com/powershell/2004/04">P2DT22H31.9085205S</TS>
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertEqual(ret.days, 2)
        self.assertEqual(ret.seconds, 22 * 60 * 60 + 31)
        self.assertEqual(ret.microseconds, 908521)
    
    def test_unsigned_byte(self):
        exampleXml = """
        <By xmlns="http://schemas.microsoft.com/powershell/2004/04">204</By>
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertEqual(ret, bytes([204]))

    def test_unsigned_short(self):
        exampleXml = """
        <U16 xmlns="http://schemas.microsoft.com/powershell/2004/04">65535</U16>
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertEqual(ret, 65535)

    def test_signed_short(self):
        exampleXml = """
        <I16 xmlns="http://schemas.microsoft.com/powershell/2004/04">-32767</I16>
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertEqual(ret, -32767)

    def test_unsigned_int(self):
        exampleXml = """
        <U32 xmlns="http://schemas.microsoft.com/powershell/2004/04">4294967295</U32>
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertEqual(ret, 4294967295)

    def test_signed_int(self):
        exampleXml = """
        <I32 xmlns="http://schemas.microsoft.com/powershell/2004/04">-2147483648</I32>
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertEqual(ret, -2147483648)

    def test_unsigned_long(self):
        exampleXml = """
        <U64 xmlns="http://schemas.microsoft.com/powershell/2004/04">18446744073709551615</U64>
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertEqual(ret, 18446744073709551615)

    def test_signed_long(self):
        exampleXml = """
        <I64 xmlns="http://schemas.microsoft.com/powershell/2004/04">-9223372036854775808</I64>
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertEqual(ret, -9223372036854775808)

    def test_float(self):
        exampleXml = """
        <Sg xmlns="http://schemas.microsoft.com/powershell/2004/04">12.34</Sg>
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertEqual(ret, 12.34)

    def test_double(self):
        exampleXml = """
        <Db xmlns="http://schemas.microsoft.com/powershell/2004/04">12.34</Db>
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertEqual(ret, 12.34)

    def test_decimal(self):
        exampleXml = """
        <D xmlns="http://schemas.microsoft.com/powershell/2004/04">12.34</D>
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertEqual(ret, 12.34)

    def test_array_of_bytes(self):
        exampleXml = """
        <BA xmlns="http://schemas.microsoft.com/powershell/2004/04">AQIDBA==</BA>
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertEqual(ret, bytes({1,2,3,4}))

    def test_guid(self):
        exampleXml = """
        <G xmlns="http://schemas.microsoft.com/powershell/2004/04">792e5b37-4505-47ef-b7d2-8711bb7affa8</G>
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertEqual(ret, uuid.UUID('792e5b37-4505-47ef-b7d2-8711bb7affa8'))
    
    def test_uri(self):
        exampleXml = """
        <URI xmlns="http://schemas.microsoft.com/powershell/2004/04">http://www.microsoft.com/</URI>
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertEqual(ret, urllib.parse.urlparse("http://www.microsoft.com/"))

    def test_nil(self):
        exampleXml = """
        <Nil xmlns="http://schemas.microsoft.com/powershell/2004/04" />
        """
        parser = ET.XMLParser(target=cli.CliXMLParser())
        parser.feed(exampleXml)
        ret = parser.close()
        self.assertEqual(ret, None)          

class TestDeltaTimeParser(unittest.TestCase):

    def test_duration2(self):
        ret = cli.parseDeltaTime("P1Y2M3DT10H30M10.10S")
        self.assertEqual(ret.days, 365 * 1 + 2 * 30 + 3)
        self.assertEqual(ret.seconds, 10 * 60 * 60 + 30 * 60 + 10)
        self.assertEqual(ret.microseconds, 10 * 10000)

    def test_duration_seconds(self):
        ret = cli.parseDeltaTime("PT31.9085205S")
        self.assertEqual(ret.days, 0)
        self.assertEqual(ret.seconds, 31)
        self.assertEqual(ret.microseconds, 908521)

if __name__ == "__main__":
    unittest.main()