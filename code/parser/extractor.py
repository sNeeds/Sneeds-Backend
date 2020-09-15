from bs4 import BeautifulSoup


class Node:
    def __init__(self, parent=None, mode=None, content=None):
        self.parent = parent
        self.mode = mode
        self.content = content


content = None

with open('majors.html', 'r') as f:
    content = f.read()

soup = BeautifulSoup(content, 'lxml')

print(soup.find_all('a'))
