import argparse
import yaml
from lxml import etree

def add_attrs(ele, **attr_dic):
    for k, v in attr_dic.items():
        if k == '_class':
            k = 'class'
        ele.attrib[k]=v
    return ele

def new_section(parent, header):
    cell = add_attrs(parent, width="32%", valign="top", _class="cheat_sheet_output_sortable cheat_sheet_output_column_1")
    section = etree.SubElement(cell,'section')
    section = add_attrs(section, _class="cheat_sheet_output_wrapper cheat_sheet_output_column_twocol",style="z-index: 30; page-break-inside: avoid;" )
    if True:
        h3 = etree.SubElement(section, 'h3')
        h3 = add_attrs(h3, _class="cheat_sheet_output_title")
        h3.text = header

        block = etree.SubElement(section,'div')
        block = add_attrs(block, _class="cheat_sheet_output_block")
        if True:
            table = etree.SubElement(section, "table")
            table = add_attrs(table, border="0", cellspacing="0", cellpadding="0", _class="cheat_sheet_output_twocol")

    return table

def add_items(parent, flag, *args):
    row_class = ["countrow","altrow countrow"]
    row = etree.SubElement(parent, 'tr')
    row = add_attrs(row, _class=row_class[flag])
    for i, value in enumerate(args):
        cell = etree.SubElement(row, 'td')
        cell = add_attrs(cell, valign="top", _class=f"cheat_sheet_output_cell_{i+1}")
        item = etree.SubElement(cell, 'div')
        item = add_attrs(item, style="padding: 3px 8px;")
        item.text = value

def add_note(parent, note):
    div = etree.SubElement(parent, 'div')
    div = add_attrs(div, _class="cheat_sheet_note", style="padding: 3px 8px;")
    div.text = note

def doit(infile):
    with open(infile) as file:
        content = yaml.load(file, Loader=yaml.FullLoader)

    table = etree.SubElement(article, "table")
    table = add_attrs(table, border="0", cellspacing="0", width="100%", cellpadding="0", _class="cheat_sheet_output")
    row = etree.SubElement(table, 'tr') 
    for _, col in enumerate(content):#.items():
        if _:
            spacer = etree.SubElement(row, 'td')
            spacer = add_attrs(spacer, _class="cheat_sheet_output_column_spacer",width="2%")
            # spacer.text = "&nbsp;"
        div_col = etree.SubElement(row, 'td')
        if content[col]:
            for header, items in content[col].items():
                if items:
                    div_section = new_section(div_col, header)
                    for i, key in enumerate(items):
                        add_items(div_section, i % 2, key, items[key])
                else: # note
                    add_note(div_col, header)
    

    with open(infile.replace(".yaml",".html"), "wb") as f:
        tree.getroot().getroottree().write(f, pretty_print=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='csmaker')
    parser.add_argument('infile', type=str, help='input markdown')
    args = parser.parse_args()

    tree = etree.parse("template.html")
    article = tree.xpath("//article")[0]
    doit(args.infile)
