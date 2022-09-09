import argparse
import yaml
from lxml import etree
import watchdog.events
import watchdog.observers
import time
import argparse

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
    tree = etree.parse("template.html")
    article = tree.xpath("//article")[0]
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

 
class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.yaml'],
                                                             ignore_directories=True, case_sensitive=False)
  
    def on_created(self, event):
        print("Watchdog received created event - % s." % event.src_path)
        # Event is created, you can process it now
        doit(event.src_path)
  
    def on_modified(self, event):
        print("Watchdog received modified event - % s." % event.src_path)
        # Event is modified, you can process it now
        doit(event.src_path)
  
  
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='csmaker')
    parser.add_argument('--src', nargs='?', type=str, default ='sheets', help='source path')
    args = parser.parse_args()

    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=args.src, recursive=True)
    observer.start()
    try:
        while True: 
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()