from lxml import etree

filename = "resistor_220.svg"
tree = etree.parse(open(filename, 'r'))

for element in tree.iter():
    if element.tag.split("}")[1] == "path":
        if element.get("stroke") == "#8C8C8C":
            yes_votes = element.get("stroke")
            print(yes_votes)

        