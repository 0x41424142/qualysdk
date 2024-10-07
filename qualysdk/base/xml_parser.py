"""
xml_parser.py - contains the xml_parser function that parses an XML string into a dictionary.
"""

from lxml.etree import _Comment
from defusedxml.lxml import fromstring


def xml_parser(xml_string, attr_prefix="@", cdata_key="#text"):
    """
    Turn an xml string into a dictionary.

     Params:
         xml_string (str): The xml string to parse.
         attr_prefix (str): The prefix to add to attributes.
         cdata_key (str): The key to use for cdata.

     Returns:
         dict: The parsed xml as a dictionary.
    """
    # check if the user passed in a string or bytes. if string, encode it to utf-8
    if isinstance(xml_string, str):
        xml_string = xml_string.encode("utf-8")

    def parse_element(element):
        parsed_dict = {}
        # Parse attributes
        for key, value in element.attrib.items():
            parsed_dict[attr_prefix + key] = value
        # Parse child elements
        for child in element:
            if isinstance(child, _Comment):
                continue  # Skip comments
            child_dict = parse_element(child)
            if child.tag in parsed_dict:
                if not isinstance(parsed_dict[child.tag], list):
                    parsed_dict[child.tag] = [parsed_dict[child.tag]]
                parsed_dict[child.tag].append(child_dict)
            else:
                parsed_dict[child.tag] = child_dict
        # Parse text content
        text = (element.text or "").strip()
        if text:
            if parsed_dict:
                parsed_dict[cdata_key] = text
            else:
                parsed_dict = text
        return parsed_dict

    root = fromstring(xml_string)
    return {root.tag: parse_element(root)}
