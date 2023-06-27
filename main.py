
f = open("test.txt", "r")
game_board = []

while (True):
    line = f.readline()
    if not line:
        break

    else:
        lst = line.split()
        for i in range(len(lst)):
            if lst[i] == 'None':
                lst[i] = None
            else:
                lst[i] = int(lst[i])

    game_board.append(lst)

#print(game_board)


class Board:
    def __init__(self, blocks):
        self.field = blocks
        self.goal = []
        self.length = len(self.field)
        for i in range(len(self.field)):
            self.goal.append([(item + 1) + (i * self.length) for item in range(self.length)])

        self.goal[-1][-1] = None

        self.lst = []

    def get_field(self):
        return self.field

    def get_length(self):
        return self.length



    def dimension(self):
        return self.length

    def hamming(self):
        count = 0
        hamming = 0

        for i in range(self.length):
            for j in range(self.length):
                count += 1
                if self.field[i][j] is not None and self.field[i][j] != count:
                    hamming += 1

        return hamming

    def manhattan(self):
        manhattan = 0

        for i in range(self.length):
            for j in range(self.length):
                if self.field[i][j] is not None:
                    manhattan += abs(((self.field[i][j] - 1) % self.length) - j) + abs(((self.field[i][j] - 1) // self.length) - i)

        return manhattan

    def isGoal(self):
        return self.field == self.goal

    def twin(self):
        self.twin = self.field[:]
        if self.twin[0][0] is not None and self.twin[0][1] is not None:
            self.twin[0][0], self.twin[0][1] = self.twin[0][1], self.twin[0][0]

        else:
            self.twin[1][0],self.twin[1][1] = self.twin[1][1], self.twin[1][0]

        return self.twin

    def __eq__(self, board):
        return self.field == board.field

    def __iter__(self):
        set_for_next = set()

        for i in range(self.length):
            for j in range(self.length):
                if self.field[i][j] is None:
                    col = j
                    row = i

                    set_for_next.add((i,j - 1))
                    set_for_next.add((i, j + 1))
                    set_for_next.add((i + 1, j))
                    set_for_next.add((i - 1, j))
                    break

        for pos in set_for_next:
            if pos[0] <= -1 or pos[0] >= self.length or pos[1] <= -1 or pos[1] >= self.length:
                pass

            else:
                copy = []
                for cop in range(self.length):
                    copy.append(self.field[cop][:])
                copy[pos[0]][pos[1]], copy[row][col] = copy[row][col], copy[pos[0]][pos[1]]
                self.lst.append(Board(copy))

        return self

    def __next__(self):

        if len(self.lst) == 0:
            raise StopIteration

        else:
            return self.lst.pop(0)

    def __str__(self):
        string = ''

        copy = []
        for cop in range(self.length):
            copy.append(self.field[cop][:])


        for i in range(self.length):
            for j in range(self.length):
                if copy[i][j] is None:
                    copy[i][j] = ' '
                    break
        for i in range(self.length):
            string += ' '.join(map(str, copy[i])) + '\n'

        return string[:-1]


class HeapItem:
    def __init__(self, brd, p, prev = None, move = 0):
        self.brd = brd
        self.priority = p
        self.prev = prev
        self.move = move

    def get_board(self):
        return self.brd

    def get_priority(self):
        return self.priority

    def get_prev(self):
        return self.prev

    def get_move(self):
        return self.move

    def __str__(self):
        string = ''

        copy = []
        for cop in range(self.brd.length):
            copy.append(self.brd.field[cop][:])

        for i in range(self.brd.length):
            for j in range(self.brd.length):
                if copy[i][j] is None:
                    copy[i][j] = ' '
                    break
        for i in range(self.brd.length):
            string += ' '.join(map(str, copy[i])) + '\n'

        return string[:-1] + '\n'


class Heap:
    # конструктор, инициализирующий все необходимые поля необходимыми значениями
    def __init__(self):
        self.heap = []
        self.tail = -1

    def left_son(self, id):
        return 2 * id + 1

    def right_son(self, id):
        return 2 * id + 2

    def parent(self, id):
        return max({0, int((id - 1) / 2)})

    def min_son(self, brd):

        id = None

        for i in range(len(self.heap)):
            if self.heap[i].brd == brd:
                id = i

        lft_sn = self.left_son(id)
        rght_sn = self.right_son(id)
        if lft_sn > len(self.heap) - 1:
            return -1

        if rght_sn <= len(self.heap) - 1:
            if self.heap[lft_sn].priority < self.heap[rght_sn].priority:
                return lft_sn

            else:
                return rght_sn

        else:
            return lft_sn

    def sift_up(self, brd):

        id = None

        for i in range(len(self.heap)):
            if self.heap[i].brd == brd:
                id = i

        if id == 0:
            return

        prnt = self.parent(id)
        # пока мы не в корне и текущий элемент меньше родительского, меняем их и поднимаемся выше

        while id != 0 and self.heap[prnt].priority > self.heap[id].priority:
            self.heap[prnt], self.heap[id] = self.heap[id], self.heap[prnt]
            id = prnt
            prnt = self.parent(id)

    def sift_down(self, brd):
        id = None

        for i in range(len(self.heap)):
            if self.heap[i].brd == brd:
                id = i

        minCh = self.min_son(brd)

        while minCh > 0 and self.heap[minCh].priority < self.heap[id].priority:
            self.heap[minCh], self.heap[id] = self.heap[id], self.heap[minCh]
            id = minCh
            minCh = self.min_son(self.heap[id].brd)

    # метод для добавления элемента x в кучу
    def add(self, brd, priority, prev, move):
        id = None

        for i in range(len(self.heap)):
            if self.heap[i].brd == brd:
                id = i

        if id is not None:
            self.change_priority(brd, priority, id, prev, move)

        else:

            self.tail += 1
            self.heap.append(HeapItem(brd, priority, prev,move))
            self.sift_up(brd)

    def change_priority(self, brd, new_priority, id, prev, move):

        if self.heap[id].priority > new_priority:
            self.heap[id].priority = new_priority
            self.heap[id].prev = prev
            self.heap[id].move = move
            self.sift_up(brd)

            # метод для возврата минимума

    def min(self):
        if self.tail == -1:
            raise Exception('error')

        return self.heap[0]

    # метод для возврата минимума и удаления его из кучи
    def get_min(self):
        if self.tail == -1:
            raise Exception('error')

        self.heap[0], self.heap[self.tail] = self.heap[self.tail], self.heap[0]
        min = self.heap.pop(self.tail)
        self.tail -= 1
        if self.tail >= 0:
            self.sift_down(self.heap[0].brd)

        return min

    # печать массива с бинарным деревом кучи
    def __str__(self):
        return '\n'.join(map(str, self.heap))

class Solver:
    def __init__(self,board,priority = 'manhattan'):
        self.brd = board
        self.p = priority
        if not (self.p == 'manhattan' or self.p == 'hamming'):
            raise Exception('wrong input')
        self.path =[]
        self.moves = 0



    def isSolvable(self):
        is_right = []
        e = None
        for i in range(self.brd.length):
            for j in range(self.brd.length):
                if self.brd.field[i][j] is None:
                    e = i + 1
                else:
                    if self.brd.field[i][j] in is_right:
                        return False
                    is_right.append(self.brd.field[i][j])

        summ = sum(self.brd.field, [])
        inversion = 0
        for i in range(self.brd.length ** 2):
            if summ[i] is None:
                summ.pop(i)
                break

        for i in range(len(summ) - 1):
            is_sorted = 1
            for j in range(len(summ) - 1):
                if summ[j] > summ[j + 1]:
                    inversion += 1
                    is_sorted = 0
                    summ[j], summ[j+1] = summ[j+1], summ[j]
            if is_sorted:
                if self.brd.length % 2 == 0:
                    return (inversion + e) % 2 == 0

                return inversion % 2 == 0

    def moves(self):
        return self.moves


    def __iter__(self):
        return self

    def __next__(self):
        if self.path == []:
            raise StopIteration

        for i in range(len(self.path)):
            return self.path.pop(i).brd

    def solve(self):
        self.moves = 0
        self.path = []
        if self.p == 'manhattan' and self.isSolvable():
            heap = Heap()
            heap.add(self.brd, self.brd.manhattan(), None, 0)
            closed = []
            goal = heap.get_min()
            closed.append(goal.brd.get_field())
            while not goal.get_board().isGoal():

                for neighbour in goal.get_board():
                    if neighbour.get_field() not in closed:
                        heap.add(neighbour, neighbour.manhattan() + goal.get_move() + 1, goal, goal.get_move() + 1)

                goal = heap.get_min()
                self.moves += 1
                closed.append(goal.get_board().get_field())

            while goal is not None:
                self.path.append(goal)
                goal = goal.get_prev()

            self.path = self.path[::-1]

        elif self.p == 'hamming' and self.isSolvable():
            heap = Heap()
            heap.add(self.brd, self.brd.hamming(), None, 0)
            closed = []
            goal = heap.get_min()
            closed.append(goal.brd.get_field())
            while not goal.get_board().isGoal():

                for neighbour in goal.get_board():
                    if neighbour.get_field() not in closed:
                        heap.add(neighbour, neighbour.hamming() + goal.get_move() + 1, goal, goal.get_move() + 1)

                goal = heap.get_min()
                self.moves += 1
                closed.append(goal.get_board().get_field())

            while goal is not None:
                self.path.append(goal)
                goal = goal.get_prev()

            self.path = self.path[::-1]


        else:
            raise Exception('unsolvable')


class Solver_2:
    def __init__(self, board, priority='manhattan'):
        self.brd = board
        self.p = priority
        if not (self.p == 'manhattan' or self.p == 'hamming'):
            raise Exception('wrong input')
        self.path = []
        self.moves = 0

    def isSolvable(self):
        is_right = []
        e = None
        for i in range(self.brd.length):
            for j in range(self.brd.length):
                if self.brd.field[i][j] is None:
                    e = i + 1
                else:
                    if self.brd.field[i][j] in is_right:
                        return False
                    is_right.append(self.brd.field[i][j])

        summ = sum(self.brd.field, [])
        inversion = 0
        for i in range(self.brd.length ** 2):
            if summ[i] is None:
                summ.pop(i)
                break

        for i in range(len(summ) - 1):
            is_sorted = 1
            for j in range(len(summ) - 1):
                if summ[j] > summ[j + 1]:
                    inversion += 1
                    is_sorted = 0
                    summ[j], summ[j + 1] = summ[j + 1], summ[j]
            if is_sorted:
                if self.brd.length % 2 == 0:
                    return (inversion + e) % 2 == 0

                return inversion % 2 == 0

    def moves(self):
        return self.moves

    def __iter__(self):
        return self

    def __next__(self):
        if self.path == []:
            raise StopIteration

        for i in range(len(self.path)):
            return self.path.pop(i).brd

    def solve(self):
        self.moves = 0
        self.path = []
        if self.p == 'manhattan' and self.isSolvable():
            list_game = []
            list_game.append(HeapItem(self.brd, self.brd.manhattan(), None, 0))
            closed = []
            goal = list_game[0]
            closed.append(goal.brd.get_field())
            while not goal.get_board().isGoal():

                for neighbour in goal.get_board():
                    if neighbour.get_field() not in closed:

                        for i in list_game:
                            if i.brd.field == neighbour.field:
                                if i.priority < neighbour.manhattan() + goal.get_move() + 1:
                                    i.priority = neighbour.manhattan() + goal.get_move() + 1
                                    i.prev = goal
                                    i.move = goal.get_move() + 1
                                    break

                        else:
                            list_game.append(HeapItem(neighbour, neighbour.manhattan() + goal.get_move() + 1, goal,
                                                      goal.get_move() + 1))

                list_game.sort(key = lambda i: i.priority)
                goal = list_game.pop(0)
                self.moves += 1
                closed.append(goal.get_board().get_field())

            while goal is not None:
                self.path.append(goal)
                goal = goal.get_prev()

            self.path = self.path[::-1]

        elif self.p == 'hamming' and self.isSolvable():
            list_game = []
            list_game.append(HeapItem(self.brd, self.brd.manhattan(), None, 0))
            closed = []
            goal = list_game[0]
            closed.append(goal.brd.get_field())
            while not goal.get_board().isGoal():

                for neighbour in goal.get_board():
                    if neighbour.get_field() not in closed:

                        for i in list_game:
                            if i.brd.field == neighbour.field:
                                if i.priority < neighbour.manhattan() + goal.get_move() + 1:
                                    i.priority = neighbour.manhattan() + goal.get_move() + 1
                                    i.prev = goal
                                    i.move = goal.get_move() + 1
                                    break

                        else:
                            list_game.append(HeapItem(neighbour, neighbour.manhattan() + goal.get_move() + 1, goal,
                                                      goal.get_move() + 1))

                list_game.sort(key=lambda i: i.priority)
                goal = list_game.pop(0)
                self.moves += 1
                closed.append(goal.get_board().get_field())

            while goal is not None:
                self.path.append(goal)
                goal = goal.get_prev()

            self.path = self.path[::-1]

        else:
            raise Exception('unsolvable')

def generator_unique_board(n, size):
    board = []
    number = 1
    for i in range(size):
        line = []
        for j in range(size):

            if (i == 0) and (j == 0):
                line.append(None)
            else:
                line.append(number)
                number += 1

        board.append(line)

    emptiness = n % (size ** 2)
    emptiness_i = 0
    while emptiness > size - 1:
        emptiness -= size
        emptiness_i += 1

    board[0][0], board[emptiness_i][emptiness] = board[emptiness_i][emptiness], board[0][0]

    index_j = 0
    while n > size:
        n //= 3
        index_j += 1
        index_i = 0

        while index_j > size - 1:
            index_j -= size
            index_i += 1

        if board[index_i][index_j] == None:
            if index_j == size - 1:

                if index_i == size - 1:
                    index_i = index_j = 0
                else:
                    index_i += 1
                    index_j = 0

            else:
                index_j += 1

        if index_j + 1 < size:
            if board[index_i][index_j + 1] != None:
                board[index_i][index_j], board[index_i][index_j + 1] = board[index_i][index_j + 1], board[index_i][
                    index_j]
            else:
                if index_j + 2 < size:
                    board[index_i][index_j], board[index_i][index_j + 2] = board[index_i][index_j + 2], board[index_i][
                        index_j]
                elif index_i + 1 < size:
                    board[index_i][index_j], board[index_i + 1][0] = board[index_i + 1][0], board[index_i][index_j]
                else:
                    board[index_i][index_j], board[0][0] = board[0][0], board[index_i][index_j]

        elif index_i + 1 < size:
            if board[index_i + 1][index_j] != None:
                board[index_i][index_j], board[index_i + 1][index_j] = board[index_i + 1][index_j], board[index_i][
                    index_j]
            else:
                if index_j + 1 < size:
                    board[index_i][index_j], board[index_i + 1][index_j + 1] = board[index_i + 1][index_j + 1], \
                                                                               board[index_i][index_j]
                elif index_i + 2 < size:
                    board[index_i][index_j], board[index_i + 2][0] = board[index_i + 2][0], board[index_i][index_j]
                else:
                    board[index_i][index_j], board[0][0] = board[0][0], board[index_i][index_j]

        else:
            board[index_i][index_j], board[0][0] = board[0][0], board[index_i][index_j]

    game_board = Board(board)
    solver = Solver(game_board)
    if solver.isSolvable():
        return game_board
    else:
        game_board.field = game_board.twin()
        return game_board

blocks = [[7,2,8],[6,4,5],[1,3,None]]
brd = Board(blocks)
solver = Solver(brd)
solver.solve()
for i in solver:
    print()
    print(i)

