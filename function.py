from utils import *

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    # print("values before reduce puzzle: ", values)
    values = reduce_puzzle(values)
    print("values after reduce puzzle: ", values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        print("solved puzzle: ", values)
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    print("n: ", n)
    print("s: ", s)
    print("values[s]: ", values[s])
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        print("new sudoku: ", new_sudoku)
        new_sudoku[s] = value
        print("new sudoku[s]: ", new_sudoku[s])
        attempt = search(new_sudoku)
        if attempt:
            # print("end")
            return attempt

# display(search(grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')))

display(search(grid_values('4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')))