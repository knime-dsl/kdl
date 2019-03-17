import sys
import os
import getopt
import jsonschema
import kdlc


def main():
    argv = sys.argv[1:]
    if len(argv) <= 2:
        print("kdlc -i <input_file> -o <output_file>")
        sys.exit(2)

    input_file = ""
    output_file = ""

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["help", "input=", "output="])
    except getopt.GetoptError:
        print("kdlc -i <input_file> -o <output_file>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("kdlc -i <input_file> -o <output_file>")
            sys.exit()
        elif opt in ("-i", "--input") and arg:
            input_file = os.path.abspath(arg)
        elif opt in ("-o", "--output") and arg:
            output_file = os.path.abspath(arg)
        else:
            print("kdlc -i <input_file> -o <output_file>")
            sys.exit()

    # Validate input arguments
    if output_file == "" or input_file == "":
        print("kdlc -i <input_file> -o <output_file>")
        sys.exit()
    if not (
        os.path.isfile(input_file)
        and input_file.endswith(".knwf")
        and output_file.endswith(".knwf")
    ):
        print("Provided file parameters don't exist or are invalid")
        sys.exit()
    output_workflow_name = os.path.splitext(os.path.basename(output_file))[0]

    # Extract workflow
    input_workflow_name = kdlc.unzip_workflow(input_file)
    input_workflow_path = f"{kdlc.INPUT_PATH}/{input_workflow_name}"

    # Parse connections from workflow.knime
    input_connection_list = kdlc.extract_connections(
        f"{input_workflow_path}/workflow.knime"
    )
    # print(input_connection_list)

    # Parse nodes from workflow.knime
    input_node_list = kdlc.extract_nodes(f"{input_workflow_path}/workflow.knime")
    # print(input_node_list)

    # Parse settings.xml for each node in workflow.knime and add to node
    for node in input_node_list:
        infile = f'{input_workflow_path}/{node["filename"]}'
        node["settings"] = kdlc.extract_from_input_xml(infile)

    # Generate and save workflow.knime in output directory
    output_workflow_path = f"{kdlc.OUTPUT_PATH}/{output_workflow_name}"

    output_workflow_knime = kdlc.create_workflow_knime_from_template(
        input_node_list, input_connection_list
    )
    kdlc.save_workflow_knime(output_workflow_knime, output_workflow_path)

    # Generate and save XML for nodes in output directory
    for node in input_node_list:
        # POC for JSON validation, uncomment below to test diff scenarios
        # if node["settings"]["name"] == "CSV Reader":
        # empty url
        # node["settings"]["model"][0]["url"] = ""
        # no url entry
        # node["settings"]["model"].pop(0)
        # update url
        # node["settings"]["model"][0]["url"] = "/path/to/other/file.csv"
        try:
            kdlc.validate_node_from_schema(node)
        except jsonschema.ValidationError as e:
            print(e.message)
            kdlc.cleanup()
            sys.exit(1)
        except jsonschema.SchemaError as e:
            print(e.message)
            kdlc.cleanup()
            sys.exit(1)
        tree = kdlc.create_node_settings_from_template(node)
        kdlc.save_node_settings_xml(tree, f'{output_workflow_path}/{node["filename"]}')

    # Zip output workflow into .knwf archive
    kdlc.create_output_workflow(output_workflow_name)


if __name__ == "__main__":
    main()
