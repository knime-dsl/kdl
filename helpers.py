import os, zipfile
from shutil import make_archive
import xml.etree.ElementTree as ET

inputpath = 'input'
outputpath = 'output'
templatepath = 'templates'
ns = {'knime': 'http://www.knime.org/2008/09/XMLConfig'}
entrytag = f'{{{ns["knime"]}}}entry'
configtag = f'{{{ns["knime"]}}}config'

# assumes workflow filename == workflow name
def unzipWorkflow(inputfile):
    zip_ref = zipfile.ZipFile(inputfile, 'r')
    zip_ref.extractall(inputpath)
    zip_ref.close()
    return os.path.splitext(inputfile)[0]

def extractFromInputXML(inputfile):
    baseTree = ET.parse(inputfile)
    root = baseTree.getroot()
    node = {}
    node['name'] = root.find("./knime:entry[@key='name']",ns).attrib['value']
    model = []
    for child in root.findall("./knime:config[@key='model']/*",ns):
        if child.tag == entrytag:
            entry = extractEntryTag(child)
            model.append(entry)
        elif child.tag == configtag:
            config = extractConfigTag(child)
            model.append(config)

    node['model'] = model
    return node

def extractEntryTag(tree):
    entry = {tree.attrib['key']: tree.attrib['value'],
             'type': tree.attrib['type']}
    return entry

def extractConfigTag(tree):
    configValue = []
    for child in tree.findall("./*",ns):
        if child.tag == entrytag:
            entry = extractEntryTag(child)
            configValue.append(entry)
        elif child.tag == configtag:
            config = extractConfigTag(child)
            configValue.append(config)
    config = {tree.attrib['key']: configValue, 'type': 'config'}
    return config

def extractNodes(inputfile):
    nodeList = []
    baseTree = ET.parse(inputfile)
    root = baseTree.getroot()
    for child in root.findall("./knime:config[@key='nodes']/knime:config",ns):
        node = {}
        nodeId = child.find("./knime:entry[@key='id']",ns).attrib['value']
        node['id'] = nodeId
        settingsFile = child.find("./knime:entry[@key='node_settings_file']",ns).attrib['value']
        node['filename'] = settingsFile
        nodeList.append(node)
    return nodeList

def extractConnections(inputfile):
    connectionList = []
    baseTree = ET.parse(inputfile)
    root = baseTree.getroot()
    for child in root.findall("./knime:config[@key='connections']/knime:config",ns):
        connection = {}
        sourceID = child.find("./knime:entry[@key='sourceID']",ns).attrib['value']
        connection['sourceID'] = sourceID
        destID = child.find("./knime:entry[@key='destID']",ns).attrib['value']
        connection['destID'] = destID
        sourcePort = child.find("./knime:entry[@key='sourcePort']",ns).attrib['value']
        connection['sourcePort'] = sourcePort
        destPort = child.find("./knime:entry[@key='destPort']",ns).attrib['value']
        connection['destPort'] = destPort
        connectionList.append(connection)
    return connectionList

def createNodeXMLFromTemplate(node):
    template = f'{templatepath}/{node["name"]}/settings_no_model.xml'
    templateTree = ET.parse(template)
    templateRoot = templateTree.getroot()
    model = templateRoot.find("./knime:config[@key='model']", ns)
    #ET.dump(model)
    for curr in node['model']:
        if curr['type'] == 'config':
            config = createConfigElement(curr)
            model.append(config)
        else:
            entry = createEntryElement(curr)
            model.append(entry)
    #ET.dump(model)
    return templateTree

def createEntryElement(entry):
    entrykey = list(entry.keys())[0]
    entryvalue = entry[entrykey]
    entrytype = entry['type']
    entryElt = ET.Element('entry', key=entrykey, type=entrytype, value=entryvalue)
    return entryElt

def createConfigElement(config):
    configkey = list(config.keys())[0]
    configvalues = config[configkey]
    configElt = ET.Element('config', key=configkey)
    for value in configvalues:
        if value['type'] == 'config':
            childConfig = createConfigElement(value)
            configElt.append(childConfig)
        else:
            childEntry = createEntryElement(value)
            configElt.append(childEntry)
    return configElt

def addConfigToTemplateModel(model, config):
    configkey = list(config.keys())[0]
    configvalues = config(configkey)
    for value in configvalues:
        if value['type'] == 'config':
            print('do something')
        else:
            entrykey = list(value.keys())[0]
            entryvalue = value[entrykey]
            entrytype = value['type']
            entry = ET.Element('entry', key=entrykey, type=entrytype, value=entryvalue)

def saveNodeXML(tree, outputpath):
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    ET.register_namespace('', ns['knime'])
    tree.write(f'{outputpath}/settings.xml', xml_declaration=True, encoding='UTF-8')

def createOutputWorkflow(workflowName):
    make_archive(f'{workflowName}_new', 'zip', outputpath)
    base = os.path.splitext(f'{workflowName}_new.zip')[0]
    os.rename(f'{workflowName}_new.zip', base + '.knwf')