import os
import zipfile
import shutil
import xml.etree.ElementTree as ET
from jinja2 import Environment, PackageLoader, select_autoescape
import tempfile
import json
import textwrap
from typing import List, Any, Dict
from kdlc.objects import Node, Connection

jinja_env = Environment(
    loader=PackageLoader("kdlc", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
    extensions=["jinja2.ext.do"],
)

TMP_INPUT_DIR = tempfile.TemporaryDirectory()
INPUT_PATH = TMP_INPUT_DIR.name
TMP_OUTPUT_DIR = tempfile.TemporaryDirectory()
OUTPUT_PATH = TMP_OUTPUT_DIR.name

NS = {"knime": "http://www.knime.org/2008/09/XMLConfig"}
ENTRY_TAG = f'{{{NS["knime"]}}}entry'
CONFIG_TAG = f'{{{NS["knime"]}}}config'


def unzip_workflow(input_file: str) -> str:
    """
    Unzips the provided workflow archive and returns the folder with
    the workflow definitions

    Args:
        input_file (str): Name of the workflow archive

    Returns:
        str: Name of the workflow folder
    """

    zip_ref = zipfile.ZipFile(input_file, "r")
    zip_ref.extractall(INPUT_PATH)
    zip_ref.close()
    return os.listdir(INPUT_PATH).pop()


def extract_from_input_xml(node_id: str, input_file: str) -> Node:
    """
    Parses the provided input file and returns a populated dict with
    associated values

    Args:
        node_id (str): Node's id from workflow.knime
        input_file (str): XML file containing a node definition

    Returns:
        dict: Dict populated with values extracted from provided input file
    """
    base_tree = ET.parse(input_file)
    root = base_tree.getroot()

    name_ele = root.find("./knime:entry[@key='name']", NS)
    if name_ele is not None:
        name = name_ele.attrib["value"]
    else:
        ex = ValueError("Input file missing name tag")
        raise ex

    factory_ele = root.find("./knime:entry[@key='factory']", NS)
    if factory_ele is not None:
        factory = factory_ele.attrib["value"]
    else:
        ex = ValueError("Input file missing factory tag")
        raise ex

    bundle_name_ele = root.find("./knime:entry[@key='node-bundle-name']", NS)
    if bundle_name_ele is not None:
        bundle_name = bundle_name_ele.attrib["value"]
    else:
        ex = ValueError("Input file missing node-bundle-name tag")
        raise ex

    bundle_symbolic_name_ele = root.find(
        "./knime:entry[@key='node-bundle-symbolic-name']", NS
    )
    if bundle_symbolic_name_ele is not None:
        bundle_symbolic_name = bundle_symbolic_name_ele.attrib["value"]
    else:
        ex = ValueError("Input file missing node-bundle-symbolic-name tag")
        raise ex

    bundle_version_ele = root.find("./knime:entry[@key='node-bundle-version']", NS)
    if bundle_version_ele is not None:
        bundle_version = bundle_version_ele.attrib["value"]
    else:
        ex = ValueError("Input file missing node-bundle-version tag")
        raise ex

    feature_name_ele = root.find("./knime:entry[@key='node-feature-name']", NS)
    if feature_name_ele is not None:
        feature_name = feature_name_ele.attrib["value"]
    else:
        ex = ValueError("Input file missing node-feature-name tag")
        raise ex

    feature_symbolic_name_ele = root.find(
        "./knime:entry[@key='node-feature-symbolic-name']", NS
    )
    if feature_symbolic_name_ele is not None:
        feature_symbolic_name = feature_symbolic_name_ele.attrib["value"]
    else:
        ex = ValueError("Input file missing node-feature-symbolic-name tag")
        raise ex

    feature_version_ele = root.find("./knime:entry[@key='node-feature-version']", NS)
    if feature_version_ele is not None:
        feature_version = feature_version_ele.attrib["value"]
    else:
        ex = ValueError("Input file missing node-feature-version tag")
        raise ex

    node = Node(
        id=node_id,
        name=name,
        factory=factory,
        bundle_name=bundle_name,
        bundle_symbolic_name=bundle_symbolic_name,
        bundle_version=bundle_version,
        feature_name=feature_name,
        feature_symbolic_name=feature_symbolic_name,
        feature_version=feature_version,
    )
    for child in root.findall("./knime:config[@key='model']/*", NS):
        if child.tag == ENTRY_TAG:
            entry = extract_entry_tag(child)
            node.model.append(entry)
        elif child.tag == CONFIG_TAG:
            config = extract_config_tag(child)
            node.model.append(config)
        else:
            ex = ValueError("Invalid settings tag")
            raise ex

    node.port_count = len(root.findall("./knime:config[@key='ports']/*", NS))

    for child in root.findall("./knime:config[@key='variables']/*", NS):
        if child.tag == CONFIG_TAG:
            config = extract_config_tag(child)
            node.variables.append(config)
        else:
            ex = ValueError("Invalid settings tag")
            raise ex
    return node


def extract_entry_tag(tree: ET.Element) -> Dict[str, Any]:
    """
    Extracts the entry tag from the provided tree

    Args:
        tree (Element): The tree to extract entry tag from

    Returns:
        dict: Dict containing the entry tag definition
    """
    entry: Dict[str, Any] = dict()
    if tree.attrib["type"] == "xstring":
        entry[tree.attrib["key"]] = tree.attrib["value"]
    elif tree.attrib["type"] == "xboolean":
        if tree.attrib["value"] == "true":
            entry[tree.attrib["key"]] = True
        else:
            entry[tree.attrib["key"]] = False
    elif tree.attrib["type"] == "xint":
        entry[tree.attrib["key"]] = int(tree.attrib["value"])
    elif tree.attrib["type"] in ["xlong", "xshort"]:
        entry[tree.attrib["key"]] = int(tree.attrib["value"])
        entry["data_type"] = tree.attrib["type"]
    elif tree.attrib["type"] == "xfloat":
        entry[tree.attrib["key"]] = float(tree.attrib["value"])
    elif tree.attrib["type"] == "xdouble":
        entry[tree.attrib["key"]] = float(tree.attrib["value"])
        entry["data_type"] = tree.attrib["type"]
    elif tree.attrib["type"] in ["xchar", "xbyte", "xpassword"]:
        entry[tree.attrib["key"]] = tree.attrib["value"]
        entry["data_type"] = tree.attrib["type"]
    else:
        ex = ValueError("Invalid entry type")
        raise ex

    if "isnull" in tree.attrib:
        entry["isnull"] = True
    return entry


def extract_config_tag(tree: ET.Element) -> dict:
    """
    Extracts the config tag from the provided tree

    Args:
        tree (Element): The tree to extract the config tag from

    Returns:
        dict: Dict containing the config tag definition
    """
    config_value = list()
    for child in tree.findall("./*", NS):
        if child.tag == ENTRY_TAG:
            entry = extract_entry_tag(child)
            config_value.append(entry)
        elif child.tag == CONFIG_TAG:
            config = extract_config_tag(child)
            config_value.append(config)
        else:
            ex = ValueError("Invalid child tag")
            raise ex
    config = {tree.attrib["key"]: config_value}
    return config


def extract_node_filenames(input_file: str) -> List[dict]:
    """
    Extracts the list of nodes from the provided KNIME workflow

    Args:
        input_file (str): Name of input workflow.knime file

    Returns:
        list: The list of node file names within the KNIME workflow
    """
    node_list = list()
    base_tree = ET.parse(input_file)
    root = base_tree.getroot()
    for child in root.findall("./knime:config[@key='nodes']/knime:config", NS):
        node = dict()
        node_id_ele = child.find("./knime:entry[@key='id']", NS)
        if node_id_ele is not None:
            node["id"] = node_id_ele.attrib["value"]
        else:
            ex = ValueError("Input file missing id")
            raise ex

        settings_file_ele = child.find("./knime:entry[@key='node_settings_file']", NS)
        if settings_file_ele is not None:
            node["filename"] = settings_file_ele.attrib["value"]
        else:
            ex = ValueError("Input file missing node_settings_file")
            raise ex

        node_list.append(node)
    return node_list


def extract_connections(input_file: str) -> List[Connection]:
    """
    Extracts a list of connections from the provided KNIME workflow

    Args:
        input_file (str): Name of input workflow.knime file

    Returns:
        list: The list of connections within the KNIME workflow
    """

    connection_list = list()
    base_tree = ET.parse(input_file)
    root = base_tree.getroot()
    for i, child in enumerate(
        root.findall("./knime:config[@key='connections']/knime:config", NS)
    ):
        source_id_ele = child.find("./knime:entry[@key='sourceID']", NS)
        if source_id_ele is not None:
            source_id = source_id_ele.attrib["value"]
        else:
            ex = ValueError("Input file missing sourceID")
            raise ex

        dest_id_ele = child.find("./knime:entry[@key='destID']", NS)
        if dest_id_ele is not None:
            dest_id = dest_id_ele.attrib["value"]
        else:
            ex = ValueError("Input file missing destID")
            raise ex

        source_port_ele = child.find("./knime:entry[@key='sourcePort']", NS)
        if source_port_ele is not None:
            source_port = source_port_ele.attrib["value"]
        else:
            ex = ValueError("Input file missing sourcePort")
            raise ex

        dest_port_ele = child.find("./knime:entry[@key='destPort']", NS)
        if dest_port_ele is not None:
            dest_port = dest_port_ele.attrib["value"]
        else:
            ex = ValueError("Input file missing destPort")
            raise ex

        connection = Connection(
            id=i,
            source_id=source_id,
            dest_id=dest_id,
            source_port=source_port,
            dest_port=dest_port,
        )
        connection_list.append(connection)
    return connection_list


def create_node_settings_from_template(node: Node) -> ET.ElementTree:
    """
    Creates an ElementTree with the provided node definition

    Args:
        node (Node): Node definition

    Returns:
        ElementTree: ElementTree populated with the provided node definition
    """
    template = jinja_env.get_template("settings_template.xml")
    for value in node.model:
        k = list(value.keys())[0]
        v = value[k]
        if type(v) is list:
            set_config_element_type(value)
        else:
            set_entry_element_type(value)

    node.extract_variables_from_model()
    template_root = ET.fromstring(template.render(node=node))
    return ET.ElementTree(template_root)


def create_workflow_knime_from_template(
    node_list: List[Node], connection_list: List[Connection]
) -> ET.ElementTree:
    """
    Creates an ElementTree with the provided node list and connection list

    Args:
        node_list (list): List of Node definitions
        connection_list (list): List of Connections amongst nodes

    Returns:
        ElementTree: ElementTree populated with nodes and their associated
        connections
    """
    template = jinja_env.get_template("workflow_template.xml")
    data = {"nodes": node_list, "connections": connection_list}
    return ET.ElementTree(ET.fromstring(template.render(data)))


def set_entry_element_type(entry: dict) -> None:
    """
    Sets an entry Element's type and value based on the provided entry definition

    Args:
        entry (dict): Entry definition

    """
    entry_key = list(entry.keys())[0]
    entry_type = type(entry[entry_key])
    entry_value = str(entry[entry_key])
    if "data_type" in entry:
        data_type = entry["data_type"]
    elif entry_type is int:
        data_type = "xint"
    elif entry_type is float:
        data_type = "xfloat"
    elif entry_type is bool:
        entry_value = entry_value.lower()
        data_type = "xboolean"
    elif entry_type is str:
        data_type = "xstring"
    else:
        ex = ValueError("Cannot set element type")
        raise ex
    entry["data_type"] = data_type
    entry[entry_key] = entry_value


def set_config_element_type(config: dict) -> None:
    """
    Sets a config Element's type based on the provided config definition

    Args:
        config (dict): Config definition

    """
    config_key = list(config.keys())[0]
    config_values = config[config_key]
    config["data_type"] = "config"
    for value in config_values:
        k = list(value.keys())[0]
        v = value[k]
        if type(v) is list:
            set_config_element_type(value)
        else:
            set_entry_element_type(value)


def save_node_settings_xml(tree: ET.ElementTree, output_path: str) -> None:
    """Writes the provided tree to the provided output path

    Args:
        tree (ElementTree): Populated ElementTree
        output_path (str): Location to write the tree to
    """
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ET.register_namespace("", NS["knime"])
    tree.write(output_path, xml_declaration=True, encoding="UTF-8")


def save_workflow_knime(tree: ET.ElementTree, output_path: str) -> None:
    """
    Writes the provided tree containing a KNIME workflow to the provided output path

    Args:
        tree (ElementTree): Populated ElementTree containing a KNIME workflow
        output_path (str): Location to write tree to
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ET.register_namespace("", NS["knime"])
    tree.write(f"{output_path}/workflow.knime", xml_declaration=True, encoding="UTF-8")


def create_output_workflow(workflow_name: str) -> None:
    """
    Bundles the provided workflow into a knwf archive

    Args:
        workflow_name (str): Workflow directory to archive
    """
    shutil.make_archive(workflow_name, "zip", OUTPUT_PATH)
    os.rename(f"{workflow_name}.zip", f"{workflow_name}.knwf")
    cleanup()


def save_output_kdl_workflow(
    output_file: str, connection_list: List[Connection], node_list: List[Node]
) -> None:
    """
    Outputs node connections and node JSON as .kdl file

    Args:
        output_file (str): Name of output kdl file
        connection_list (list): list of Connections to be written
        node_list (list): list of Nodes to be written
    """

    wrapper = textwrap.TextWrapper(
        initial_indent="\t", subsequent_indent="\t", width=120
    )
    with open(output_file, "w") as file:
        file.write("Nodes {\n")
        for node in node_list:
            settings = node.__dict__.copy()
            settings.pop("id")
            settings.pop("variables")
            output_text = f"(n{node.id}): {json.dumps(settings, indent=4)}"
            for line in output_text.splitlines():
                wrapped = wrapper.fill(line)
                file.write(f"{wrapped}\n")
            file.write("\n")
        file.write("}\n\n")
        file.write("Workflow {\n")
        for connection in connection_list:
            if connection.source_port == "0" and connection.dest_port == "0":
                wrapped = wrapper.fill(
                    f"(n{connection.source_id})~~>" f"(n{connection.dest_id})\n"
                )
            else:
                wrapped = wrapper.fill(
                    f"(n{connection.source_id}:{connection.source_port})-->"
                    f"(n{connection.dest_id}:{connection.dest_port})\n"
                )
            file.write(f"{wrapped}\n")
        file.write("}\n")


def cleanup() -> None:
    """
    Cleans up temp directories

    """
    TMP_INPUT_DIR.cleanup()
    TMP_OUTPUT_DIR.cleanup()
