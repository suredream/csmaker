import argparse
import yaml
from lxml import etree

def addTag(parent, name, **attr_dic):
    ele = etree.SubElement(parent, name)
    for k, v in attr_dic.items():
        if k == '_class':
            k = 'class'
        ele.attrib[k] = v
    return ele

def new_section(parent, header):
    section = addTag(parent, 'section', _class="cheat_sheet_output_wrapper cheat_sheet_output_column_twocol",
                     style="z-index: 30; page-break-inside: avoid;")
    if True:
        h3 = addTag(section, 'h3', _class="cheat_sheet_output_title")
        h3.text = header
        block = addTag(section, 'div', _class="cheat_sheet_output_block")
        if True:
            table = addTag(block, "table", border="0", cellspacing="0",
                           cellpadding="0", _class="cheat_sheet_output_twocol",
                           id="cheat_sheet_output_table")
    return table


def add_items(parent, flag, *args):
    row_class = ["countrow", "altrow countrow"]
    row = addTag(parent, 'tr', _class=row_class[flag])
    for i, value in enumerate(args):
        cell = addTag(row, 'td', valign="top",
                      _class=f"cheat_sheet_output_cell_{i+1}")
        item = addTag(cell, 'div', style="padding: 3px 8px;")
        if value and value.startswith('http'):
            link = addTag(item, 'a', href=value)
            link.text = "link"
        else:
            item.text = value

def add_note(parent, note):
    div = addTag(parent, 'div', _class="cheat_sheet_note",
                 style="padding: 3px 8px;")
    div.text = note


def doit(infile):
    with open(infile) as file:
        content = yaml.load(file, Loader=yaml.FullLoader)

    table = addTag(article, "table", border="0", cellspacing="0",
                   width="100%", cellpadding="0", _class="cheat_sheet_output")
    row = addTag(table, 'tr')
    for _, col in enumerate(content):  # .items():
        if _:
            spacer = addTag(
                row, 'td', _class="cheat_sheet_output_column_spacer", width="2%")
        div_col = addTag(row, 'td', width="32%", valign="top",
                         _class="cheat_sheet_output_sortable cheat_sheet_output_column_1")
        if content[col]:
            for header, items in content[col].items():
                if items:
                    div_section = new_section(div_col, header)
                    for i, key in enumerate(items):
                        add_items(div_section, i % 2, key, items[key])
                else:  # note
                    add_note(div_col, header)

    with open(infile.replace(".yaml", ".html"), "wb") as f:
        tree.getroot().getroottree().write(f, pretty_print=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='csmaker')
    parser.add_argument('infile', type=str, help='input markdown')
    args = parser.parse_args()

    tree = etree.parse("template.html")
    article = tree.xpath("//article")[0]
    doit(args.infile)
