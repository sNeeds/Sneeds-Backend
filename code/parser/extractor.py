from bs4 import BeautifulSoup


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
current_h4_node = None

with open('majors.html', 'r') as f:
    content = f.read()


def check_and_add_h2_header(e):
    if e.name == 'h2':
        global current_h2_node
        global current_h3_node
        global current_h4_node

        node = Node(e.span.get_text())
        current_h2_node = node

        current_h3_node = None
        current_h4_node = None


def check_and_add_h3_header(e):
    if e.name == 'h3':
        global current_h3_node
        global current_h4_node

        text = e.select("span.mw-headline")[0].get_text()
        node = Node(text, parent=current_h2_node)
        current_h3_node = node

        current_h4_node = None


def check_and_add_h4_header(e):
    if e.name == 'h4':
        global current_h4_node
        text = e.select("span.mw-headline")[0].get_text()
        node = Node(text, parent=current_h3_node)


def check_and_add_table_list(e):
    if e.name == 'div':
        if e.table:
            tr = e.tbody.tr
            for td in tr.find_all("td", recursive=False):
                lists = td.ul.find_all("li", recursive=False)
                if current_h4_node:
                    parent = current_h4_node
                else:
                    parent = current_h3_node
                import_lists(lists, parent)


def import_lists(lists, parent=None):
    for l in lists:
        if l.ul is None:
            Node(l.a.get_text(), parent=parent)
        else:
            node = Node(l.a.get_text(), parent=parent)

            lists = l.ul.find_all("li", recursive=False)
            import_lists(lists, node)
            # print(lists)


soup = BeautifulSoup(content, 'lxml')

main_body = soup.select('body div#content div#bodyContent div#mw-content-text div.mw-parser-output')[0]

for e in main_body.children:
    if e.name:
        check_and_add_h2_header(e)
        check_and_add_h3_header(e)
        check_and_add_h4_header(e)
        check_and_add_table_list(e)

for n in nodes_list:
    print(n)
