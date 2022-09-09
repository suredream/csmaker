import argparse
import os
import yaml




#     doit(args.infile)
import sys
from lxml import etree

def add_attrs(ele, **attr_dic):
    for k, v in attr_dic.items():
        if k == '_class':
            k = 'class'
        ele.attrib[k]=v
    return ele


def new_col(parent):
    table = etree.SubElement(parent, "table")
    table = add_attrs(table, border="0", cellspacing="0", width="100%", cellpadding="0", _class="cheat_sheet_output")
    row = etree.SubElement(table, 'tr')
    cell = etree.SubElement(row, 'td')
    return cell

def new_header(parent, header):
    section = etree.SubElement(parent,'section')
    section = add_attrs(section, _class="cheat_sheet_output_wrapper cheat_sheet_output_column_twocol",style="z-index: 30; page-break-inside: avoid;" )
    h3 = etree.SubElement(section, 'h3')
    h3 = add_attrs(h3, _class="cheat_sheet_output_title")
    h3.text = header
    block = etree.SubElement(section,'div')
    block = add_attrs(block, _class="cheat_sheet_output_block")

    table2 = etree.SubElement(block, "table")
    table2 = add_attrs(table2, border="0", cellspacing="0", cellpadding="0", _class="cheat_sheet_output_twocol")
    row2 = etree.SubElement(table2, 'tr')
    row2 = add_attrs(row2, _class="altrow countrow")

    return row2

    return cell2

def add_items(parent, *args):
    for i, value in enumerate(args):
        cell2 = etree.SubElement(parent, 'td')
        cell2 = add_attrs(cell2, valign="top", _class=f"cheat_sheet_output_cell_{i+1}")
        item = etree.SubElement(cell2, 'div')
        item = add_attrs(item, style="padding: 3px 8px;")
        item.text = value


def doit(infile):
    with open(infile) as file:
        content = yaml.load(file, Loader=yaml.FullLoader)

    for i_col, col in content.items():
        ip = new_col(article) 
        # colTable = add_attrs(table, border="0", cellspacing="0", width="100%", cellpadding="0", _class="cheat_sheet_output")
        if col:
            for header, items in col.items():
                # add header
                ip = new_header(ip, header)
                # block = etree.Element("table")
                for key, value in items.items():
                    cellTable = etree.Element("table")
                    add_items(ip, key, value)
                    # print(key, value)
        #         colTable.append(block)
        # article.append(colTable)
    with open("out.html", "wb") as f:
        tree.getroot().getroottree().write(f, pretty_print=True)

# if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='csmaker')
    # parser.add_argument('infile', type=str, help='input markdown')
    # args = parser.parse_args()

tree = etree.parse("template.html")
article = tree.xpath("//article")[0]
doit('example.yaml')