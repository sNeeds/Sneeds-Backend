from bs4 import BeautifulSoup


class Node:
    def __init__(self, content, parent=None):
        self.parent = parent
        self.content = content

    def __str__(self):
        name = self.content
        if self.parent:
            name +=  " -> " + self.parent.__str__()
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
        node = Node(e.span.get_text())
        nodes_list.append(node)
        current_h2_node = node


def check_and_add_h3_header(e):
    if e.name == 'h3':
        global current_h3_node
        text = e.select("span.mw-headline")[0].get_text()
        node = Node(text, parent=current_h2_node)
        nodes_list.append(node)
        current_h3_node = node


def check_and_add_h4_header(e):
    if e.name == 'h4':
        global current_h4_node
        text = e.select("span.mw-headline")[0].get_text()
        node = Node(text, parent=current_h3_node)
        nodes_list.append(node)
        current_h4_node = node


soup = BeautifulSoup(content, 'lxml')

main_body = soup.select('body div#content div#bodyContent div#mw-content-text div.mw-parser-output')[0]

for e in main_body.children:
    if e.name:
        check_and_add_h2_header(e)
        check_and_add_h3_header(e)
        check_and_add_h4_header(e)

for n in nodes_list:
    print(n)
