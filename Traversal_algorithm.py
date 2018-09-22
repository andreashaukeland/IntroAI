import os
from Node import Node


# Create a new map from input file
def set_up_map(filename):
    board = initialize_board(filename)
    make_graph(board)
    return board


# Creates a 2D-array filled with nodes
def initialize_board(filename):
    file = open(os.getcwd() + "/boards/" + filename, "r")
    board_array = []
    for line in file:
        line = line.strip("\n")
        row = []
        for char in line:
            new_node = Node(char)
            row.append(new_node)
        board_array.append(row)
    return board_array


# Connects all the nodes in the array and calculates heuristic cost
def make_graph(board):
    start_node = get_start_node(board)
    start_node.travel_cost = start_node.cost
    goal_row, goal_column = get_goal_node_coordinates(board)

    for row in range(len(board)):
        for column in range(len(board[row])):
            node = board[row][column]
            node.row = row
            node.column = column

            # Calculate the heuristic cost
            node.heuristic_cost = calculate_heuristic_cost(row, column, goal_row, goal_column)

            # Add all the Nodes neighbours
            if row != 0 and not board[row - 1][column].blocked:
                node.neighbours.append(board[row - 1][column])
            if row != len(board) - 1 and not board[row + 1][column].blocked:
                node.neighbours.append(board[row + 1][column])
            if column != 0 and not board[row][column - 1].blocked:
                node.neighbours.append(board[row][column - 1])
            if column != len(board[row]) - 1 and not board[row][column + 1].blocked:
                node.neighbours.append(board[row][column + 1])


# Pretty print of board
def print_board(board):
    for row in board:
        output_string = ""
        for column in row:
            output_string += str(column)
        print(output_string)
    print()


# Returns start node from board if it exists
def get_start_node(board):
    for row in board:
        for node in row:
            if node.start_node:
                return node


# Returns coordinates of goal node
def get_goal_node_coordinates(board):
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column].goal_node:
                return row, column


# Calculate heuristic costs according to Manhatten path
def calculate_heuristic_cost(current_row, current_column, goal_row, goal_column):
    return abs(current_row - goal_row) + abs(current_column - goal_column)


# A-star algorithm for shortest path
def a_star(start_node):
    return traversal_algorithm(start_node)


# BFS algorithm. Keeps a FIFO queue by never sorting.
def bfs(start_node):
    return traversal_algorithm(start_node, sort=False)


# Dijkstra algorithm. Ignores heuristic cost.
def dijkstra(start_node):
    return traversal_algorithm(start_node, calculate_heuristic_costs=False)


# General traversal algorithm that can implement A-star, BFS and Dijkstra.
def traversal_algorithm(start_node, sort=True, calculate_heuristic_costs=True):
    travelling_queue = [start_node]  # A sorted list of most promising nodes
    visited_nodes = {start_node: []}  # The path of nodes to visit a node

    while not travelling_queue == []:
        current_node = travelling_queue.pop(0)  # Gets the current best node

        if current_node.goal_node:
            return visited_nodes[current_node], visited_nodes

        for node in current_node.neighbours:
            # We have to reset heuristic cost for the Dijkstra algorithm.
            if not calculate_heuristic_costs:
                node.heuristic_cost = 0

            if node not in visited_nodes:
                # Makes hard-copy of parent node path and extends with current-node
                path_to_parent_node = list(visited_nodes[current_node])
                path_to_parent_node.append(current_node)
                visited_nodes[node] = path_to_parent_node

                node.travel_cost = current_node.travel_cost + node.cost
                travelling_queue.append(node)
        # If we want to expand by most promising node, we have to sort after each iteration
        if sort:
            travelling_queue.sort()


input_filename = "board-2-4.txt"
board = set_up_map(input_filename)
start_node = get_start_node(board)
print_board(board)

# Traversal algorithm
travel_list, visited_nodes = a_star(start_node)

# Make it easy to see path we have chosen
for element in travel_list:
    element.on_path = True
print_board(board)

# Check which elements we have checked out
for element in visited_nodes:
    element.visited = True
print_board(board)


