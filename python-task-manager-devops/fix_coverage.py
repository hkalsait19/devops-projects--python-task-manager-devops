import xml.etree.ElementTree as ET

def fix_coverage(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Remove unsupported attributes
    if "version" in root.attrib:
        del root.attrib["version"]
    if "timestamp" in root.attrib:
        del root.attrib["timestamp"]

    # Write the fixed file back
    tree.write(file_path, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    fix_coverage("coverage.xml")