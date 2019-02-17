import xml.etree.ElementTree as ET
import dateutil.parser as du
import datetime as dt
import re

class CliXMLParser:
    schema_name = "{http://schemas.microsoft.com/powershell/2004/04}"
    lastNode = None
    stack = []
    currentData = None
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

        if (node != node): 
            self.stack[-1].append(node)
        self.lastNode = node
    def data(self, data):
        self.currentData = data
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

if __name__ == "__main__":

    print(parseDeltaTime("PT31.9085205S"))

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

