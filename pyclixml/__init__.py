import xml.etree.ElementTree as ET
import dateutil.parser as du
import datetime as dt
import re
import base64
import uuid
import urllib.parse

class CliXMLParser:
    schema_name = "{http://schemas.microsoft.com/powershell/2004/04}"
    lastNode = None
    stack = []
    currentData = ""
    def start(self, tag, attrib):
        #print("tag=" + tag + " start. stack=")
        #print(self.stack)
        if (tag == self.schema_name + "Objs"):
            self.stack.append([])
        if (tag == self.schema_name + "Obj"):
            self.stack.append([])
    def end(self, tag):
        node = None
        if (tag == self.schema_name + "Objs"):
            self.lastPop = self.stack.pop()
            node = self.lastPop
        elif (tag == self.schema_name + "Obj"):
            self.lastPop = self.stack.pop()
            node = self.lastPop
        elif (tag == self.schema_name + "S"):
            node = self.currentData
        elif (tag == self.schema_name + "C"):
            node = chr(int(self.currentData))
        elif (tag == self.schema_name + "B"):
            if (self.currentData == "true"):
                node = True
            elif (self.currentData == "false"):
                node = False
        elif (tag == self.schema_name + "DT"):
            node = du.parse(self.currentData)
        elif (tag == self.schema_name + "TS"):
            node = parseDeltaTime(self.currentData)
        elif (tag == self.schema_name + "By"):
            node = bytes([int(self.currentData)])
        # unspport signed byte
        #elif (tag == self.schema_name + "SB"):
        #    node = bytes([int(self.currentData)])
        elif (tag == self.schema_name + "U16"):
            node = int(self.currentData)
        elif (tag == self.schema_name + "I16"):
            node = int(self.currentData)
        elif (tag == self.schema_name + "U32"):
            node = int(self.currentData)
        elif (tag == self.schema_name + "I32"):
            node = int(self.currentData)
        elif (tag == self.schema_name + "U64"):
            node = int(self.currentData)
        elif (tag == self.schema_name + "I64"):
            node = int(self.currentData)
        elif (tag == self.schema_name + "Sg"):
            node = float(self.currentData)
        elif (tag == self.schema_name + "Db"):
            node = float(self.currentData)
        elif (tag == self.schema_name + "D"):
            node = float(self.currentData)
        elif (tag == self.schema_name + "BA"):
            node = base64.b64decode(self.currentData)
        elif (tag == self.schema_name + "G"):
            node = uuid.UUID(self.currentData)
        elif (tag == self.schema_name + "URI"):
            node = urllib.parse.urlparse(self.currentData)
        elif (tag == self.schema_name + "Nil"):
            node = None
        elif (tag == self.schema_name + "Version"):
            node = parseVersion(self.currentData)
        elif (tag == self.schema_name + "XD"):
            node = ET.fromstring(self.currentData)
        
        self.currentData = "" 
    
        if (node != node): 
            self.stack[-1].append(node)
        self.lastNode = node

    def data(self, data):
        self.currentData += data

    def close(self):
        return self.lastNode

def parseDeltaTime(s):
    pattern = r"(?P<minus>-?)P(?P<year>\d+Y)?(?P<mouth>\d+M)?(?P<day>\d+D)?T?(?P<hour>\d+H)?(?P<minitus>\d+M)?(?P<seconds>[\d.]+S)?"
    results = re.match(pattern, s, re.S)

    days = 0
    groupdict = results.groupdict()
    year = groupdict["year"]
    if year != None:
        days += int(year[:-1]) * 365
    
    mouth = groupdict["mouth"]
    if mouth != None:
        days += int(mouth[:-1]) * 30
    
    day = groupdict["day"]
    if day != None:
        days += int(day[:-1])

    seconds = 0
    hour = groupdict["hour"]
    if hour != None:
        seconds += int(hour[:-1]) * 60 * 60
    
    minitus = groupdict["minitus"]
    if minitus != None:
        seconds += int(minitus[:-1]) * 60

    sseconds = groupdict["seconds"]
    if sseconds != None:
        seconds += float(sseconds[:-1])

    return dt.timedelta(days=days, seconds=seconds) 

class Version:
    def __init__(self, major=0, minor=0, build=-1, revision=-1):
        self.major = major
        self.minor = minor
        self.build = build
        self.revision = revision

def parseVersion(s):
    sp = s.split('.')
    if (len(sp) == 2):
        return Version(major=int(sp[0]), minor=int(sp[1]))
    elif (len(sp) == 3):
        return Version(major=int(sp[0]), minor=int(sp[1]), build=int(sp[2]))
    elif (len(sp) == 4):
        return Version(major=int(sp[0]), minor=int(sp[1]), build=int(sp[2]), revision=int(sp[3]))
    else:
        raise ValueError("Invalid Version string => " + s )

if __name__ == "__main__":

    #print(parseDeltaTime("PT31.9085205S"))
    exampleXml = """
    <XD xmlns="http://schemas.microsoft.com/powershell/2004/04">
        &lt;name attribute="value"&gt;Content&lt;/name&gt;
    </XD>
    """
    print(exampleXml)
    parser = ET.XMLParser(target=CliXMLParser())
    parser.feed(exampleXml)
    ret = parser.close()

    print(ret)

    #target = CliXMLParser()
    #parser = ET.XMLParser(target=target)

    #parser.feed(exampleXml)
    #ret = parser.close()
    #print(ret)
    #exampleXml = """
    #<DT xmlns="http://schemas.microsoft.com/powershell/2004/04">2019-02-14T21:44:13.419689+09:00</DT>
    #"""
    #parser = ET.XMLParser(target=CliXMLParser())
    #parser.feed(exampleXml)
    #ret = parser.close()
    #print(ret)
    #print(type(ret))
    pass

