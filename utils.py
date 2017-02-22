rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s + t for s in a for t in b]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + col_units + square_units

# diagonal sudoku
# diagonal1 = [a[0]+a[1] for a in zip(rows, cols)]
# diagonal2 = [a[0]+a[1] for a in zip(rows, cols[::-1])]
# unitlist.append(diagonal1)
# unitlist.append(diagonal2)

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

print("boxes: ", boxes)
print("row_units: ", row_units)
print("col_units: ", col_units)
print("square_units: ", square_units)
# print("diagonal1: ", diagonal1)
# print("diagonal2: ", diagonal2)
print("unitlist: ", unitlist)
print("units: ", units)
print("peers: ", peers)


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """

    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))


def eliminate(values):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # TODO: Implement only choice strategy here
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def naked_twin(values):
    twin_digits = []
    for box in values:
        if len(values[box]) == 2 and values[box] not in twin_digits:
            twin_digits.append(values[box])
            print("box: ", box, "with twin digits: ", values[box])
            print("twin_digits: ", twin_digits)
            print("twin digit length: ", len(twin_digits))

            # enumerate create tuple (0, '69')
            # for t in enumerate((twin_digits)):
            #     print("t: ", t)

            # doesn't work - can't split a list
            # for t in twin_digits:
            #     print("t: ", t)

            # need to iterate twin_digits if there's more than 1 twin_digits
            # for c in twin_digits[0]:
            #     print("c value: ", c)
            #     for peer in peers[t]:
            #         print("peer: ", peer)
            #         values[peer] = values[peer].replace(c, '')

    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        print("original values: ", values)
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        print("number of solved values before: ", solved_values_before)
        # Use the Eliminate Strategy
        values = eliminate(values)
        print("solved values after elimination: ", values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        print("solved values after only_choice: ", values)
        # Use Naked Twin Strategy
        values = naked_twin(values)
        print("solved values after naked_twin: ", values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        print("number of solved values after: ", solved_values_after)
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    print("values from reduce puzzle function: ", values)
    return values