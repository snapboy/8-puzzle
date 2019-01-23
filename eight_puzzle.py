#/usr/bin/env python3
# -*- coding: utf-8 -*-

import heapq
import copy

def initialize():
    node = []
    print("Please enter your puzzle, the blank is represented by 0\n")
    row_1 = input("Please enter your first row, use space between numbers:\n")
    temp = []
    for i in range(3):
        temp.append(int(row_1.replace('\n','').split()[i]))
    node.append(temp)
    row_2 = input("Please enter your second row, use space between numbers:\n")
    temp = []
    for i in range(3):
        temp.append(int(row_2.replace('\n','').split()[i]))
    node.append(temp)
    row_3 = input("Please enter your third row, use space between numbers:\n")
    temp = []
    for i in range(3):
        temp.append(int(row_3.replace('\n','').split()[i]))
    node.append(temp)
    return node

def print_node(node):
    for i in range(3):
        s = str(node[i][0])
        for j in range(2):
            s += ' ' + str(node[i][j + 1])
        print(s + '\n')

def misplaced_tiles(node):
    count = 0
    for i in range(8):
        if node[i // 3][i % 3] != i + 1:
            count += 1
    return count

def manhattan_distance(node):
    sum = 0
    for i in range(3):
        for j in range(3):
            if node[i][j] != 0:
                x = (node[i][j] - 1) // 3
                y = (node[i][j] - 1) % 3
                sum += (abs(x - i) + abs(y - j))
    return sum

def expand(item, nodes, algo, depth):
    i, j, x, y = 0, 0, 0, 0
    fn = item[0]
    now_node = item[1]
    print_node(now_node)
    last_action = item[2]
    #find the blank tile
    for x in range(3):
        for y in range(3):
            if now_node[x][y] == 0:
                i, j = x, y
                break
    #search its successors
    #blank goes up
    node = copy.deepcopy(now_node)
    if i > 0 and last_action != 3:
        node[i][j] = now_node[i - 1][j]
        node[i - 1][j] = now_node[i][j]
        if algo == 1:
            fn = depth + 1
        elif algo == 2:
            fn = depth + 1 + misplaced_tiles(node)
        elif algo == 3:
            fn = depth + 1 + manhattan_distance(node)
        heapq.heappush(nodes, [fn, node, 1])
    #blank goes left
    node = copy.deepcopy(now_node)
    if j > 0 and last_action != 2:
        node[i][j] = now_node[i][j - 1]
        node[i][j - 1] = now_node[i][j]
        if algo == 1:
            fn = depth + 1
        elif algo == 2:
            fn = depth + 1 + misplaced_tiles(node)
        elif algo == 3:
            fn = depth + 1 + manhattan_distance(node)
        heapq.heappush(nodes, [fn, node, 4])
    #blank goes down
    node = copy.deepcopy(now_node)
    if i < 2 and last_action != 1:
        node[i][j] = now_node[i + 1][j]
        node[i + 1][j] = now_node[i][j]
        if algo == 1:
            fn = depth + 1
        elif algo == 2:
            fn = depth + 1 + misplaced_tiles(node)
        elif algo == 3:
            fn = depth + 1 + manhattan_distance(node)
        heapq.heappush(nodes, [fn, node, 3])
    #blank goes right
    node = copy.deepcopy(now_node)
    if j < 2 and last_action != 4:
        node[i][j] = now_node[i][j + 1]
        node[i][j + 1] = now_node[i][j]
        if algo == 1:
            fn = depth + 1
        elif algo == 2:
            fn = depth + 1 + misplaced_tiles(node)
        elif algo == 3:
            fn = depth + 1 + manhattan_distance(node)
        heapq.heappush(nodes, [fn, node, 2])
    return nodes

def goal_test(node):
    for i in range(8):
        if node[i // 3][i % 3] != i + 1:
            return False
    return True

def main():
    #initialize
    print("Welcome to Jiaqi's 8-puzzle solver. Choose a way to start:")
    print("1. Start with the default puzzle")
    print("2. Start with your own puzzle")

    puzzle = int(input())
    nodes = []
    heapq.heapify(nodes)
    node = []
    if puzzle == 1:
        node = [[8, 7, 1], [6, 0, 2], [5, 4, 3]]
    elif puzzle == 2:
        node = initialize()
    #print_node(node)
    
    #choose the searching algorithm
    print("Choose a searching algorithm:")
    print("1. Uniform Cost Search")
    print("2. A* with Misplaced Tiles heuristic")
    print("3. A* with Manhattan Distance heuristic")
    algo = int(input())

    fn, gn, hn, depth = 0, 0, 0, 0
    flag = False
    if algo == 1:
        fn = 0
    elif algo == 2:
        gn = 0
        hn = misplaced_tiles(node)
        fn = gn + hn
    elif algo == 3:
        gn = 0
        hn = manhattan_distance(node)
        fn = gn + hn
    heapq.heappush(nodes, [fn, node, 0])
    while len(nodes) != 0:
        item = heapq.heappop(nodes)
        if goal_test(item[1]):
            flag = True
            break
        nodes = expand(item, nodes, algo, depth)
        depth += 1

        #for z in range(len(nodes)):
        #    print(nodes[z])
    if flag:
        print("Goal Reached!")
    else:
        print("No Path to Goal!")

if __name__ == '__main__':
    main()
