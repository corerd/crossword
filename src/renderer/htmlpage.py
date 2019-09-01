'''HTML template to show crossword puzzles

MIT License
-----------
Copyright (c) 2019 Corrado Ubezio
https://github.com/corerd

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

HTML_PAGE_HEAD = '''
<!DOCTYPE html>
<html lang="en">
<html>
<head>
<meta charset="UTF-8">
<title>Crossword Viewer</title>
<meta name="author" content="Corrado Ubezio https://github.com/corerd">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
.column {
  float: left;
  padding: 10px;
}
.clearfix::after {
  content: "";
  clear: both;
  display: table;
}
table, th, td {
  border: 1px solid black;
}
th, td {
  padding: 5px;
}
#blockcell {
  background-color: black;
}
</style>
</head>
<body>
'''

HTML_PAGE_TAIL = '''
</body>
</html>
'''

HTML_HEADING = '<h{hd}>{0}</h{hd}>'

HTML_TABLE_OPEN  = '<table>'
HTML_TABLE_CLOSE = '</table>'

HTML_TABLE_ROW_OPEN  = '<tr">'
HTML_TABLE_ROW_CLOSE = '</tr>'

HTML_TABLE_CELL = '<td{bg}><small><sup>{0}</sup></small>{1}</td>'

BLOCKCELL_DEFAULT_ID = '#'


class HtmlPage:
    '''HTML Basic Page Template providing methods to write macro elements
    to HTML document.

    This class is implemented as a context manager in order to ensure
    writing the HTML end tag in a `with` statement.
    '''

    def __init__(self, html_document_name):
        '''Opens html_document_name file writing the HTML page prologue
        including metadata and styles
        '''
        self.html_document_name = html_document_name
        self.html_file = open(html_document_name, 'w')
        self.html_file.write(HTML_PAGE_HEAD)
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.finalize()

    def finalize(self):
        '''Writes HTML page epilogue and closes the document'''
        self.html_file.write(HTML_PAGE_TAIL)
        self.html_file.close()

    def crossword(self, blockcell_id=None):
        '''Returns crossword context manager'''
        return self.Crossword(self.html_file, blockcell_id)

    def column_container(self):
        '''Returns column_container context manager'''
        return self.ColumnContainer(self.html_file)

    def column(self):
        '''Returns column context manager'''
        return self.Column(self.html_file)

    def heading(self, level, text):
        '''Writes heading'''
        print(HTML_HEADING.format(text, hd=level), file=self.html_file)

    def line(self, text):
        '''Writes a single line with terminator'''
        print(text+'<br>', file=self.html_file)
    
    def rights(self, text):
        '''Writes acknowledgements'''
        print('<p>&copy; Copyright {}</p>'.format(text), file=self.html_file)

    class Column:
        '''HtmlPage Context Manager Inner Class
        
        Defines a DIV element floating to the left of its container 
        '''

        def __init__(self, html_file_descriptor):
            '''Saves the file descriptor of an already opened document
            and writes start HTML DIV tag
            '''
            self.fd = html_file_descriptor
            print('<div class="column">', file=self.fd)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            '''Writes end HTML DIV tag'''
            print('</div>', file=self.fd)

    class ColumnContainer:
        '''HtmlPage Context Manager Inner Class

        Defines a DIV element floating columns side by side.
        It is also used the clearfix hack to take care of the layout flow.
        '''

        def __init__(self, html_file_descriptor):
            '''Saves the file descriptor of an already opened document
            and writes start HTML DIV tag
            '''
            self.fd = html_file_descriptor
            print('<div class="clearfix">', file=self.fd)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            '''Writes end HTML DIV tag'''
            print('</div>', file=self.fd)

    class Crossword:
        '''HtmlPage Context Manager Inner Class

        Renders the crossboard grid as sn HTML TABLE
        '''

        def __init__(self, html_file_descriptor, blockcell_id=None):
            '''Saves the file descriptor of an already opened document
            and writes start HTML TABLE tag

            blockcell_id is the character identifyeng shaded squares
            '''
            self.fd = html_file_descriptor
            if blockcell_id is None:
                self.blockcell_id = BLOCKCELL_DEFAULT_ID
            else:
                self.blockcell_id = blockcell_id
            print(HTML_TABLE_OPEN, file=self.fd)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            '''Writes end HTML TABLE tag'''
            print(HTML_TABLE_CLOSE, file=self.fd)

        def add_row(self, cell_list):
            '''Writes a row of cell_list to the crossword grid

            Every cell is a tuple (clue_reference, letter).
            clue_reference is the clue number of the answer
            to which letter belongs.
            '''
            print(HTML_TABLE_ROW_OPEN, file=self.fd)
            for cell in cell_list:
                color = ''  # default
                apex = cell[0]  # clue_reference
                letter = cell[1]
                if apex == self.blockcell_id:
                    color = ' id="blockcell"'
                else:
                    apex = int(apex)
                    if apex == 0:
                        apex = '&nbsp;&nbsp;'
                    else:
                        apex = '{}'.format(apex)
                        if len(apex) < 2:
                            apex = '&nbsp;' + apex
                if letter == ' ':
                    letter = '&nbsp;'
                print(HTML_TABLE_CELL.format(apex, letter, bg=color), file=self.fd)
            print(HTML_TABLE_ROW_CLOSE, file=self.fd)
