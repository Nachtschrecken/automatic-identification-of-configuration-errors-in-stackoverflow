# Formatting the dataset to better read the posts

import xml.etree.ElementTree as ET

def extract_xml_elements(xml_path, text_file_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    i = 262

    with open(text_file_path, 'a') as text_file:
        for element in root:
            text_file.write("ID: " + element.get('Id') + ", Number: " + str(i) + "\n" + element.get('Body') + '\n\n')
            i += 1

xml_path = 'Posts/negatives_full.xml'
text_file_path = 'Posts/dataset.txt'

extract_xml_elements(xml_path, text_file_path)
