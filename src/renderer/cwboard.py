'''Crossword board representation

Provides a data structure that can be rendered in an HTML file.

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

from ntpath import splitext
from .htmlpage import HtmlPage

class CrosswordBoard:
    def __init__(self, raw_list):
        if type(raw_list) is str:
            self.setPuzzle_from_file(raw_list)
        else:
            self.setPuzzle_from_labels(raw_list)
        self.clues_h = {}
        self.clues_v = {}

    def setPuzzle_from_file(self, file_path):
        '''Builds an empty puzzle board from text file_path
        '''
        self.puzzle_origin = file_path
        self.puzzle_file_path = file_path
        self.puzzle = ()
        with open(self.puzzle_file_path, 'r') as label_list:
            puzzle_cols = -1
            for label_row in label_list:
                clue_references = label_row.strip().split('\t')
                if puzzle_cols < 0:
                    # get the number of columns from the first row
                    puzzle_cols = len(clue_references)
                # every row must have the same number of columns
                assert puzzle_cols == len(clue_references)
                row = ()
                for ref in clue_references:
                    row = row + ([ref, ' '],)  # solution left empty
                self.puzzle = self.puzzle + (row,)

    def setPuzzle_from_labels(self, label_list):
        '''Builds an empty puzzle board from label_list'''
        self.puzzle_origin = 'builtin'  # default
        self.puzzle_file_path = None
        self.puzzle = ()
        for clue_references in label_list:
            row = ()
            for ref in clue_references:
                row = row + ([ref, ' '],)  # solution left empty
            self.puzzle = self.puzzle + (row,)

    def setSolution(self, position_list, solution_list):
        '''Fill the puzzle cells with the word characters of the solution

        Each solution word position is given by a list of tuples:
            (len, isVertical, clue_ref, (row,col))
        '''
        # there must be a position for each word in the solution
        assert len(position_list) == len(solution_list)
        solution_idx = 0
        for word in solution_list:
            position = position_list[solution_idx]
            # the len of word solution must match its position
            assert len(word) == position[0]
            row = position[3][0]
            col = position[3][1]
            clue_ref = position[2]
            # clue reference must match
            assert int(self.puzzle[row][col][0]) == clue_ref
            isVertical = position[1]
            if isVertical:
                self.clues_v[clue_ref] = ' '
            else:
                self.clues_h[clue_ref] = ' '
            for char_idx in range(len(word)):
                cell_value = self.puzzle[row][col][1]  # current cell value
                new_cell_value = chr(word[char_idx])
                assert cell_value == ' ' or cell_value == new_cell_value
                self.puzzle[row][col][1] = new_cell_value  # fill cell value
                if isVertical:
                    row = row + 1
                else:
                    col = col + 1
            solution_idx = solution_idx + 1

    def updateClues(self, number_tuple, clue):
        '''Updates the clue referenced by number_tuple

        number_tuple consists of (isVerticalOriented, number)
        '''
        if number_tuple[0] is True:
            self.clues_v[number_tuple[1]] = clue
        else:
            self.clues_h[number_tuple[1]] = clue

    def render(self, html_file_name=None):
        if html_file_name is None:
            if self.puzzle_file_path is not None:
                html_file_name, _ = splitext(self.puzzle_file_path)
                html_file_name = html_file_name + '.html'
        if html_file_name is None:
            return None
        with HtmlPage(html_file_name) as draw:
            draw.heading(1, 'Crossword Solver')
            draw.heading(2, 'Origin: {}'.format(self.puzzle_origin))

            # draw the empty crossword board
            with draw.crossword() as grid:
                for row in self.puzzle:
                    grid.add_row([(cell[0], ' ') for cell in row])

            # container to hold clues
            with draw.column_container() as _:
                # disply ACROSS clues
                with draw.column() as _:
                    draw.heading(3, 'ACROSS')
                    for number in self.clues_h:
                        draw.line('{} {}'.format(number, self.clues_h[number]))
                
                # disply DOWN clues
                with draw.column() as _:
                    draw.heading(3, 'DOWN')
                    for number in self.clues_v:
                        draw.line('{} {}'.format(number, self.clues_v[number]))

            # draw solution
            draw.heading(2, 'Solution')
            with draw.crossword() as grid:
                for row in self.puzzle:
                    grid.add_row([cell for cell in row])

            # draw credits
            draw.rights(
            '@ccebrecos & @davidlj in <a href="https://uab.cat/enginyeria">ETSE</a>, UAB'
            )

        return html_file_name
