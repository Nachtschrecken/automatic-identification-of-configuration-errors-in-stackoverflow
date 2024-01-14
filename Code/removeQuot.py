# Refines XML by putting every row element in one line and removing syntax-breaking 
# quotation marks from the Body or Title attribute
#
# 2023, Ferris Kleier


def format_int(number):
    format_string = "%04d" % number
    return format_string


def get_lines(filename):
    with open(filename, "r") as file:
        lines = []
        while True:
            line = file.readline()
            if not line:
                break
            lines.append(line)
    return lines


def line_formatter(heap):
    fullrow = ""
    for line in heap:
        fullrow = fullrow + line.replace("\n", " ")
    # replace in body when OwnerUserId
    if "OwnerUserId=" in fullrow:
        start_positon = fullrow.find("Body=") + 6
        end_position = fullrow.find(" OwnerUserId=") - 1
        fullrow = fullrow[:start_positon] + \
            fullrow[start_positon:end_position].replace('"', "'") + \
            fullrow[end_position:]
    else:
        start_positon = fullrow.find("Body=") + 6
        end_position = fullrow.find(" LastActivityDate=") - 1
        fullrow = fullrow[:start_positon] + \
            fullrow[start_positon:end_position].replace('"', "'") + \
            fullrow[end_position:]
    # replace in Title
    if 'PostTypeId="1"' in fullrow:
        start_positon = fullrow.find("Title=") + 7
        end_position = fullrow.find(" Tags=") - 1
        fullrow = fullrow[:start_positon] + \
            fullrow[start_positon:end_position].replace('"', "'") + \
            fullrow[end_position:]
    return fullrow

def writexml(rows):
    with open("optisliced/posts{x}.xml".format(x=x), "w") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write("<posts>\n")
        for row in rows:
            f.write(row + "\n")
        f.write("</posts>\n")

if __name__ == "__main__":
    for x in range(1):
        x = format_int(x)
        heap = []
        rows = []
        lines = get_lines("sliced/posts{x}.xml".format(x=x))
        for line in lines:
            if line.startswith("  <row"):
                heap.append(line)
            elif line.endswith("/>\n"):
                heap.append(line)
                rows.append(line_formatter(heap))
                heap = []
            elif len(heap) > 0:
                heap.append(line)
        writexml(rows)
        rows = []
        print("Finished Set {x}".format(x=x))