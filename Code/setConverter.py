# Converting the collection of links into xml
# It iterates over a simple text file with pasted elements for each row
# Removes duplicates
# Structure in: Title, post ID, URL
#
# 2023, Ferris Kleier

import re


def remove_number(url):
    if url.endswith('/'):
        url = url[:-1]
    pattern = r'\d+$'
    match = re.search(pattern, url)
    if match:
        url = url[:match.start()]
    return url


def extract_title(url):
    parts = url.split('/')
    if len(parts) > 0:
        last_part = parts[-1]
        last_part = re.sub(r'\d+$', '', last_part)
        title = last_part.replace('-', ' ').title()
        return title
    return ''


def extract_id(url):
    pattern = r'questions/(\d+)/'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return ''


def create_xml(file_path, output_file):
    with open(file_path, 'r') as text_file:
        lines = text_file.readlines()

    unique_urls = set()
    processed_lines = []
    for line in lines:
        url = line.strip()
        url_without_number = remove_number(url)
        if url_without_number not in unique_urls:
            unique_urls.add(url_without_number)
            processed_lines.append(url_without_number)

    xml_content = ''
    for url in processed_lines:
        id = extract_id(url)
        title = extract_title(url)
        xml_content += f'    <object Id="{id}" Title="{title}">{url}</object>\n'

    with open(output_file, 'w') as xml_file:
        xml_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        xml_file.write('<root>\n')
        xml_file.write(xml_content)
        xml_file.write('</root>\n')


text_file_path = 'Posts/positives.txt'
output_xml_file = 'Posts/positives.xml'

create_xml(text_file_path, output_xml_file)
