# Script to extract the relevant posts for the training and test set from the corpus
# Creates a text file with just the bodies for the model process
#
# 2023, Ferris Kleier

import xml.etree.ElementTree as ET


SIZE = 1584
MODE = "positives"
# MODE = "negatives"


def format_int(number):
    format_string = "%04d" % number
    return format_string


def load_ids(filename):
    ids = []
    with open(filename, 'r') as f:
        tree = ET.parse(f)
        root = tree.getroot()
        for element in root:
            ids.append(int(element.attrib['Id']))
    ids = set(ids)
    return list(ids)


def match_ids(ids, filename):
    full_positives = []
    with open(filename, 'r') as f:
        for line in f:
            for id in ids:
                if ' Id="{id}"'.format(id=id) in line:
                    full_positives.append(line)
    return full_positives


def write_line(line, filename):
    with open(filename, 'a') as f:
        f.write(line)


def parse_posts(origin, destination):
    with open(origin, 'r') as f:
        for line in f:
            if "<row" in line:
                start_positon = line.find("Body=") + 6
                end_position = line.find(" OwnerUserId=") - 1
                body = line[start_positon:end_position] + "\n"

                write_line(body, destination)


def labeled_sets():
    full_set = []
    with open("Posts/positives_body.txt", 'r') as f:
        for line in f:
            full_set.append([line, True])
    with open("Posts/negatives_body.txt", 'r') as f:
        for line in f:
            full_set.append([line, False])
    return full_set


# create an XML file with all the bodies and their labels
def full_dataset():
    full_set = labeled_sets()
    filename = 'array.xml'

    body = f'<?xml version="1.0" encoding="UTF-8"?>\n<posts>\n'
    write_line(body,filename)
    for post in full_set:
        text = (post[0].rstrip()).replace('"',"'")
        label = post[1]
        body = f'  <post text="{text}" label="{label}"/>\n'
        write_line(body,filename)


# ids = load_ids('Posts/{mode}.xml'.format(mode=MODE))
# ids.sort()


# full_positives = []
# for x in range(SIZE):
#     x = format_int(x)
#     full_positives = match_ids(
#         ids, 'Posts/optisliced/posts{x}.xml'.format(x=x))
#     for line in full_positives:
#         write_line(line, 'Posts/{mode}_full.xml'.format(mode=MODE))
#     print("Finished posts{x}".format(x=x))


# parse_posts('Posts/{mode}_full.xml'.format(mode=MODE),
#             'Posts/{mode}_body.txt'.format(mode=MODE))


full_dataset()