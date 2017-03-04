rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s + t for s in a for t in b]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + col_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

print("boxes: ", boxes)
print("row_units: ", row_units)
print("col_units: ", col_units)
print("square_units: ", square_units)
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
    # print("Grid in grid_values: ", grid)
    for c in grid:
        # print("c in grid: ", c)
        if c == '.':
            values.append(all_digits)
            # print("values in grid_values: ", values)
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
    # print("solved values in eliminate: ", values)
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
        # print("unit inside only_choice", unit)
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            # print("dplace: ", dplaces)
            if len(dplaces) == 1:
                values[dplaces[0]] = digit

    return values

def naked_twin(values):
    twins = []
    for k1, v1 in values.items():
        if len(v1) == 2:
            for k2, v2 in values.items():
                if k1 == k2:
                    break
                if v1 == v2 and v1 not in twins:
                    twins.append(v1)
                    # print("found matching twin digit: ", twins)

    for twin in twins:
        # print("twin: ", twin)
        for i in twin:
            # print("i: ", i)
            for box in units:
                # print("box: ", box)
                # print("value: ", values[box])
                for value in values[box]:
                    if values == i:
                        # print("value: ", value)
                        values[box] = values[box].replace(i, '')

    # print("values after naked twin: ", values)
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
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the Naked Twin Strategy
        values = naked_twin(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values