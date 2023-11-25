import heapq

# 3D matrix representation of current board state
board = [[[0, 0, 0] for x in range(3)] for y in range(3)]

# hashmap representation of goal || key (int): 0-26, value (tuple): (x, y, z) coordinates
goal = {}

# coordinate of blank || [x, y, z]
blank = [0, 0, 0]

# sequence of moves || [A1, A2, A3 ...]
moves = []

# sequence of f(n) || [f(1), f(2), f(3) ...]
f = []

# set of visited states || {board1, board2, board3 ...}
visited = set()

# nodes to be visited represented as a tuple: (f(n), order of expansion, depth, list(moves), list(f(n)), tuple(board), list(blank))
heap = []
heapq.heapify(heap)

# # of nodes generated
nodes = 1


# reads from input file and sets up initial states
def setup():
    # name your input file "input.txt"
    input = open("input.txt", "r")

    # set initial board
    for i in range(3):
        for j in range(3):
            line = input.readline().split()
            for k in range(3):
                board[i][j][k] = line[k]
                # set blank
                if line[k] == "0":
                    blank[0], blank[1], blank[2] = i, j, k
        input.readline()

    # set goal
    for i in range(3):
        for j in range(3):
            line = input.readline().split()
            for k in range(3):
                goal[line[k]] = (i, j, k)
        input.readline()

    input.close()


# searches for goal
def search():
    # initial h(n) and f(n)
    h = calc_dist()

    # add initial state to heap
    heapq.heappush(
        heap,
        (
            h,  # f(n)
            1,  # nth node
            0,  # depth
            [],  # sequence of moves
            [h],  # sequence of f(n)
            tuple(
                tuple(tuple(tuple(y) for y in board[x]) for x in range(3))
            ),  # tuple version of board
            blank.copy(),  # blank coords [x, y, z]
        ),
    )

    # add initial node to set of visited nodes
    visited.add(tuple(tuple(tuple(tuple(y) for y in board[x]) for x in range(3))))

    # test_file = open("test.txt", "w") # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< UNCOMMENT ALL LINES WITH <<<<<< TO WRITE TEST FILE

    # break when goal found
    while True:
        # status(test_file) # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< UNCOMMENT ALL LINES WITH <<<<<< TO WRITE TEST FILE

        # get node with smallest f(n) and order of expansion
        curr = heapq.heappop(heap)

        # update current state with new board, blank, moves, and f
        update_state(curr[5], curr[6], curr[3], curr[4])

        # when h(n) == depth, h(n) = 0 and goal is found
        if curr[0] == curr[2]:
            # test_file.close() # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< UNCOMMENT ALL LINES WITH <<<<<< TO WRITE TEST FILE
            break

        # try the possible actions (north, south, east, west, up, down)
        action(curr[2])

    # write result to output
    output(curr[2])


# set board = board_tup and blank = new_blank, moves = new_moves, f = new_f
def update_state(board_tup, new_blank, new_moves, new_f):
    for i in range(3):
        for j in range(3):
            for k in range(3):
                # update board
                board[i][j][k] = board_tup[i][j][k]
        # update blank
        blank[i] = new_blank[i]

    # update moves
    for i in range(len(new_moves)):
        if i < len(moves):
            moves[i] = new_moves[i]
        else:
            # new_moves is longer than moves
            moves.append(new_moves[i])

    # moves is longer than new_moves
    while len(moves) > len(new_moves):
        moves.pop()

    # update f
    for i in range(len(new_f)):
        if i < len(f):
            f[i] = new_f[i]
        else:
            # new_f is longer than f
            f.append(new_f[i])

    # f is longer than new_f
    while len(f) > len(new_f):
        f.pop()


# perform every possible action (north, south, east, west, up, down)
def action(curr_depth):
    # value in actions will be added to one of the coordinates (x, y, z) to "move" in a direction
    actions = (-1, 1)

    # 0 = x, 1 = y, 2 = z
    for i in range(3):
        for move in actions:
            # need to remember coordinates of blank from before movement
            prev_blank = blank.copy()
            blank[i] += move

            # update sequence of moves
            update_move(i, move)

            # check that movement is valid and does not go out of range
            if 0 <= blank[i] <= 2:
                generate_node(prev_blank, curr_depth)

            # revert blank and moves
            blank[i] -= move
            moves.pop()


# add correct move based on coordinate (x, y, z) and direction (forward, backward)
def update_move(coord, dir):
    match coord:
        # x
        case 0:
            match dir:
                # backward
                case -1:
                    moves.append("U")
                # forward
                case 1:
                    moves.append("D")
        # y
        case 1:
            match dir:
                # backward
                case -1:
                    moves.append("N")
                # forward
                case 1:
                    moves.append("S")
        # z
        case 2:
            match dir:
                # backward
                case -1:
                    moves.append("W")
                # forward
                case 1:
                    moves.append("E")


# creates and adds a new node to the heap and visited set
def generate_node(prev_blank, curr_depth):
    global nodes

    # move blank to new location by swapping 
    (
        board[prev_blank[0]][prev_blank[1]][prev_blank[2]],
        board[blank[0]][blank[1]][blank[2]],
    ) = (
        board[blank[0]][blank[1]][blank[2]],
        board[prev_blank[0]][prev_blank[1]][prev_blank[2]],
    )

    # convert board to tuple so it can be stored in visited set
    board_tup = tuple(tuple(tuple(tuple(y) for y in board[x]) for x in range(3)))

    # only add node to heap if not visited already
    if board_tup not in visited:
        nodes += 1
        curr_depth += 1
        visited.add(board_tup)
        h = calc_dist()

        # heap sorted by f(n), then by order of expansion
        heapq.heappush(
            heap,
            (
                (
                    h + curr_depth, # f(n)
                    nodes, # nth node
                    curr_depth, # depth
                    moves.copy(), # sequence of moves
                    f + [h + curr_depth], # sequence of f(n)
                    board_tup, # tuple version of board
                    blank.copy(), # blank coords [x, y, z]
                )
            ),
        )

    # move blank back to original location
    (
        board[prev_blank[0]][prev_blank[1]][prev_blank[2]],
        board[blank[0]][blank[1]][blank[2]],
    ) = (
        board[blank[0]][blank[1]][blank[2]],
        board[prev_blank[0]][prev_blank[1]][prev_blank[2]],
    )


# calculate manhattan distance of board
def calc_dist():
    dist = 0
    for x in range(3):
        for y in range(3):
            for z in range(3):
                # get (x, y, z) of num in goal board
                goal_x, goal_y, goal_z = goal[board[x][y][z]]
                dist += abs(x - goal_x) + abs(y - goal_y) + abs(z - goal_z)
    return dist


# writes to output file
def output(depth):
    output = open("output.txt", "w")

    # write initial state and goal
    with open("input.txt", "r") as input:
        output.write(input.read() + "\n\n")
    input.close()

    # write depth
    output.write(str(depth) + "\n\n")

    # write nodes
    output.write(str(nodes) + "\n\n")

    # write sequence of moves
    for i in moves:
        output.write(f"{i} ")
    output.write("\n\n")

    # write sequence of f(n)
    for i in f:
        output.write(f"{i} ")
    output.write("\n\n")

    output.close()


# debug functions -------------------------------------------------------------------------------------------------------------------------------------------


# writes current board, heap, and goal to test.txt
def status(test_file):
    print_board(None, test_file)
    test_file.write("------------------------------------------------------\n")
    print_heap(test_file)
    test_file.write("------------------------------------------------------\n")
    print_goal(test_file)
    test_file.write("------------------------------------------------------\n")


# prints heap, if file passed in then writes to file instead
def print_heap(test_file=None):
    print("Heap: \n") if test_file == None else test_file.write("Heap:\n\n")
    sorted_heap = heapq.nsmallest(len(heap), heap)
    for i in range(len(sorted_heap)):
        print(
            f"{i+1}. f(n): {sorted_heap[i][0]}, Node: {sorted_heap[i][1]}, Depth: {sorted_heap[i][2]}, Moves: {sorted_heap[i][3]}, Blank: {sorted_heap[i][6]}\n"
        ) if test_file == None else test_file.write(
            f"{i+1}. f(n): {sorted_heap[i][0]}, Node: {sorted_heap[i][1]}, Depth: {sorted_heap[i][2]}, Moves: {sorted_heap[i][3]}, Blank: {sorted_heap[i][6]}\n\n"
        )
        print_board(sorted_heap[i][5], test_file)


# prints current board state, if file passed in then writes to file instead
def print_board(board_tup=None, test_file=None):
    if board_tup == None:
        print("Current Board:\n") if test_file == None else test_file.write(
            "Current Board:\n\n"
        )
        for i in board:
            for j in i:
                print(j) if test_file == None else test_file.write(str(j) + "\n")
            print() if test_file == None else test_file.write("\n")
        print(f"Blank: {blank}\n") if test_file == None else test_file.write(
            f"Blank: {blank}\n"
        )
        print(f"Moves: {moves}\n") if test_file == None else test_file.write(
            f"Moves: {moves}\n"
        )
        print(f"f(n): {f}\n") if test_file == None else test_file.write(f"f(n): {f}\n")
    else:
        for i in board_tup:
            for j in i:
                print(f"   {j}") if test_file == None else test_file.write(f"   {j}\n")
            print() if test_file == None else test_file.write("\n")


# prints goal, if file passed in then writes to file instead
def print_goal(test_file=None):
    print("Goal:\n") if test_file == None else test_file.write("Goal:\n\n")
    goal_keys = list(goal.keys())
    curr = []
    ind = 0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                curr.append(goal_keys[ind])
                ind += 1
            print(curr) if test_file == None else test_file.write(str(curr) + "\n")
            curr = []
        print() if test_file == None else test_file.write("\n")


if __name__ == "__main__":
    setup()
    # print_board()
    # print_goal()
    search()
    # print_board()
    # print_goal()
