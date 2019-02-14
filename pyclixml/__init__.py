import xml.etree.ElementTree as ET

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
        if (tag == self.schema_name + "Obj"):
            self.lastPop = self.stack.pop()
            node = self.lastPop
        if (tag == self.schema_name + "S"):
            node = self.currentData
        if (tag == self.schema_name + "C"):
            node = self.currentData
        if (tag == self.schema_name + "B"):
            if (self.currentData == "true"):
                node = True
            if (self.currentData == "false"):
                node = False
        if (node != node): 
            self.stack[-1].append(node)
        self.lastNode = node
    def data(self, data):
        self.currentData = data
    def close(self):
        return self.lastNode

if __name__ == "__main__":
    target = CliXMLParser()
    parser = ET.XMLParser(target=target)

    exampleXml = """
    <S xmlns="http://schemas.microsoft.com/powershell/2004/04">This is String</S>
    """

    parser.feed(exampleXml)
    ret = parser.close()
    print(ret)