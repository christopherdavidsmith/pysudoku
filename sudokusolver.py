import copy
from termcolor import colored


class SudokuSolver:
    '''
    '''

    def __init__(self, sudoku):
        '''
        '''
        self.original = copy.deepcopy(sudoku)
        self.rows = copy.deepcopy(sudoku)

    def is_valid(self, rows=None):
        '''
        '''
        if rows is None:
            rows = self.rows

        columns = self._transpose(rows)
        squares = []

        for rindex in [0, 3, 6]:
            for cindex in [0, 3, 6]:
                squares.append(self._return_square(rows, rindex, cindex))

        for numbers_list in [rows, columns, squares]:
            for numbers in numbers_list:
                if self._are_numbers_valid(numbers) is False:
                    return False

        return True

    def _transpose(self, list_to_transpose):
        '''
        '''
        return list(map(list, zip(*list_to_transpose)))

    def _are_numbers_valid(self, numbers):
        '''
        '''
        seen_numbers = []
        for number in numbers:
            if number in seen_numbers:
                return False

            if number is not 0:
                seen_numbers.append(number)

        return True

    def brute_force(self):
        '''
        '''
        self.rows = self._solve_recursively(self.rows)[0]

    def _solve_recursively(self, rows):
        '''
        '''
        for row_index, row in enumerate(rows):
            for col_index, number in enumerate(row):
                if number is 0:

                    possible_values = self._return_missing_numbers(rows, row_index, col_index)
                    if not possible_values:
                        possible_values = range(1, 10)

                    for possible_value in possible_values:

                        rows[row_index][col_index] = possible_value
                        valid_guess = self.is_valid(rows)

                        if valid_guess:
                            tmp_rows, valid = self._solve_recursively(rows)

                            if valid is True:
                                return tmp_rows, True

                        if possible_value is possible_values[-1]:
                            rows[row_index][col_index] = 0
                            return rows, False

        return rows, True

    def _return_square(self, rows, row_index, column_index):
        '''
        '''
        row_index_start = row_index - (row_index % 3)
        col_index_start = column_index - (column_index % 3)

        square = []
        for row in rows[row_index_start:row_index_start + 3]:
            for number in row[col_index_start:col_index_start + 3]:
                square.append(number)

        return square

    def _return_missing_numbers(self, rows, row_index, column_index):
        '''
        '''
        columns = self._transpose(rows)
        square = self._return_square(rows, row_index, column_index)

        seen_numbers = []
        for numbers in [rows[row_index], columns[column_index], square]:
            for number in numbers:
                if number is not 0 and number not in seen_numbers:
                    seen_numbers.append(number)

        missing_numbers = []
        for number in range(1, 10):
            if number not in seen_numbers:
                missing_numbers.append(number)

        return missing_numbers

    def pretty_print(self):

        '''
        '''
        # Decoration
        border_decoration = " +------+------+------+"
        filled_row = " |{} {} {} |{} {} {} |{} {} {} |"

        output = ["", border_decoration]

        for row_index, row in enumerate(self.rows):

            numbers = []
            for column_index, number in enumerate(row):

                if self.original[row_index][column_index] != self.rows[row_index][column_index]:
                    number = colored(number, 'red', attrs=['bold'])

                if number == 0:
                    number = "."

                numbers.append(number)

            output.append(filled_row.format(*numbers))

            if row_index in [2, 5]:
                output.append(border_decoration)

        output.append(border_decoration)
        output.append("")

        for line in output:
            print(line)
