# Slices down big XML files into shorter chunks
# Specify desired chunk size in CHUNK_SIZE or with -M
# python3 slicer.py posts.xml -o ./sliced/ -M 5000
#
# 2023, Ferris Kleier

import os
import xml.parsers.expat
from xml.sax.saxutils import escape
from optparse import OptionParser
from math import log10

CHUNK_SIZE = 512 * 512
MAX_SIZE = (256*256)*3
FMT = ".%d"

path = []
cur_size = 0
cur_idx = 0
cur_file = None
out_dir = None
root = None
ext = None
xml_declaration = None
start = None
ending = False


def attrs_s(attrs):

    l = ['']
    for i in range(0, len(attrs), 2):
        l.append('%s="%s"' % (attrs[i], escape(attrs[i+1])))

    return ' '.join(l)


def next_file():

    global cur_size, ending

    if (not ending) and (cur_size > MAX_SIZE):

        global cur_file, cur_idx
        print("part %d Done" % cur_idx)
        ending = True

        for elem in reversed(path):
            end_element(elem[0])

        cur_file.close()
        cur_size = 0
        cur_idx += 1
        cur_file = open(os.path.join(out_dir, root + FMT %
                        cur_idx + ext), 'wt', encoding='utf8')

        if xml_declaration is not None:
            cur_file.write('<?xml%s?>\n' % attrs_s(xml_declaration))

        for elem in path:
            start_element(*elem)

        ending = False


def xml_decl(version, encoding, standalone):

    global xml_declaration
    l = ['version', version, 'encoding', encoding]
    if standalone != -1:
        l.extend(['standalone', 'yes' if standalone else 'no'])
    xml_declaration = l

    cur_file.write('<?xml%s?>\n' % attrs_s(xml_declaration))


def start_element(name, attrs):

    global cur_size, start
    if start is not None:
        # Chaining starts after each others
        cur_file.write('<%s%s>' % (start[0], attrs_s(start[1])))

    start = (name, attrs)
    if ending:
        return

    cur_size += len(name) + sum(len(k) for k in attrs)
    path.append((name, attrs))


def end_element(name):

    global cur_size
    global start

    if start is not None:
        cur_file.write('<%s%s/>' % (start[0], attrs_s(start[1])))
    else:
        cur_file.write('</%s>' % name)

    start = None
    if ending:
        return

    elem = path.pop()
    assert elem[0] == name
    cur_size += len(name)

    next_file()


def char_data(data):

    global cur_size, start

    wroteStart = False
    if start is not None:
        cur_file.write('<%s%s>' % (start[0], attrs_s(start[1])))
        start = None
        wroteStart = True

    data = data.replace('&', '&amp;')
    data = data.replace('<', '&lt;')

    if data == '>':
        data = '&gt;'

    cur_file.write(data)
    cur_size += len(data)

    if not wroteStart:
        next_file()


def main(filename, output_dir):

    p = xml.parsers.expat.ParserCreate()
    p.ordered_attributes = 1
    p.XmlDeclHandler = xml_decl
    p.StartElementHandler = start_element
    p.EndElementHandler = end_element
    p.CharacterDataHandler = char_data

    global cur_file, cur_idx
    global out_dir, root, ext

    global FMT
    FMT = ".%%0%dd" % (int(log10(os.path.getsize(filename) / MAX_SIZE)) + 1)

    out_dir, filename = os.path.split(filename)
    if output_dir is not None:
        out_dir = output_dir

    root, ext = os.path.splitext(filename)
    cur_file = open(os.path.join(out_dir, root + FMT %
                    cur_idx + ext), 'wt', encoding="utf8")

    with open(filename, 'rt', encoding="utf8") as xml_file:
        while True:
            chunk = xml_file.read(CHUNK_SIZE)
            if len(chunk) < CHUNK_SIZE:
                p.Parse(chunk, 1)
                break
            p.Parse(chunk)

    cur_file.close()

    print("part %d Done" % cur_idx)


if __name__ == "__main__":

    parser = OptionParser(usage="usage: %prog [options] XML_FILE")

    parser.add_option("-o", "--output-dir",
                      help="Specify the directory where the xml files will be written"
                      "(default to the same directory where the original file is)")
    parser.add_option("-M", "--max_size", type="int",
                      help="Specify the size at which the files should be split (in Kb)")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("incorrect number of arguments")

    if options.max_size is not None:
        MAX_SIZE = options.max_size * 1024

    main(args[0], options.output_dir)
