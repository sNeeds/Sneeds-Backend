import os

from bs4 import BeautifulSoup

from abroadin.settings.settings import BASE_DIR


class Node:
    def __init__(self, content, parent=None):
        self.parent = parent
        self.content = content
        nodes_list.append(self)

    def __str__(self):
        name = self.content
        if self.parent:
            name += " -> " + self.parent.__str__()
        return name


content = None

nodes_list = []

current_h2_node = None
current_h3_node = None
current_h4_h5_node = None

html_dir = os.path.join(BASE_DIR, "apps/data/account/management/commands/majors/majors.html")
with open(html_dir, 'r') as f:
    content = f.read()


def check_and_add_h2_header(e):
    if e.name == 'h2':
        global current_h2_node
        global current_h3_node
        global current_h4_h5_node

        node = Node(e.span.get_text())
        current_h2_node = node

        current_h3_node = None
        current_h4_h5_node = None


def check_and_add_h3_header(e):
    if e.name == 'h3':
        global current_h3_node
        global current_h4_h5_node

        text = e.select("span.mw-headline")[0].get_text()
        node = Node(text, parent=current_h2_node)
        current_h3_node = node

        current_h4_h5_node = None


def check_and_add_h4_h5_header(e):
    if e.name == 'h4' or e.name == 'h5':
        global current_h4_h5_node
        text = e.select("span.mw-headline")[0].get_text()
        node = Node(text, parent=current_h3_node)
        current_h4_h5_node = node


def check_and_add_table_list(e):
    if e.name == 'div':
        if e.table:
            tr = e.tbody.tr
            for td in tr.find_all("td", recursive=False):
                if len(td.p.find_all("b")) != 0:
                    ps = td.find_all("p", recursive=False)
                    lists = td.find_all("ul", recursive=False)
                    for i, p in enumerate(ps, start=0):
                        if p.b is None:
                            continue

                        node = Node(p.get_text(), current_h4_h5_node or current_h3_node)
                        import_lists(lists[i].find_all("li"), node)
                else:
                    lists = td.ul.find_all("li", recursive=False)
                    import_lists(lists, current_h4_h5_node or current_h3_node)


def check_and_add_direct_ul_list(e):
    if e.name == 'ul':
        lists = e.find_all('li', recursive=False)
        import_lists(lists, current_h4_h5_node or current_h3_node)


def import_lists(lists, parent=None):
    for l in lists:
        if l.ul is None:
            Node(l.a.get_text(), parent=parent)
        else:
            node = Node(l.a.get_text(), parent=parent)
            lists = l.ul.find_all("li", recursive=False)
            import_lists(lists, node)


def get_nodes():
    soup = BeautifulSoup(content, 'lxml')

    main_body = soup.select('body div#content div#bodyContent div#mw-content-text div.mw-parser-output')[0]

    for e in main_body.children:
        if e.name == 'h2' and e.span.get_text() == "See also":
            break
        check_and_add_h2_header(e)
        check_and_add_h3_header(e)
        check_and_add_h4_h5_header(e)
        check_and_add_table_list(e)
        check_and_add_direct_ul_list(e)

    return nodes_list
