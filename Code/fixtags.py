# A small script to fix XML issues caused by false syntax
# Removes duplicate Body content and pruned the XML element to original format
#
# 2023, Ferris Kleier

SIZE = 1584


def format_int(number):
    format_string = "%04d" % number
    return format_string


def fix_line(line):
    start_positon = line.find("Title=") + 7
    end_position = line.find(" Tags=") - 1
    line = line[:start_positon] + \
        "Missing Title" + \
        line[end_position:]
    return line


def writexml(rows):
    with open("optisliced/posts{x}.xml".format(x=x), "w") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write("<posts>\n")
        for row in rows:
            f.write(row)
        f.write("</posts>\n")


def bodyex(line):
    start_positon = line.find("Body=") + 6
    end_position = line.find(" OwnerUserId=") - 1
    return line[start_positon:end_position]


for x in range(SIZE):
    x = format_int(x)
    rows = []
    with open("sliced/posts{x}.xml".format(x=x), "r") as f:
        for line in f:
            # if (line.count("OwnerDisplayName=")) > 1:
            #     row = fix_line(line)
            #     rows.append(row)
            if ("Tags" in bodyex(line)) and ('PostTypeId="1"' in line):
                row = fix_line(line)
                rows.append(row)
            elif "row" in line:
                rows.append(line)
        writexml(rows)
    print("Finished {x}".format(x=x))
