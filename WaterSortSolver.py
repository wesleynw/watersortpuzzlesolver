class Vial:    
    capacity = 4
    def __init__(self, colors: list):
        self.colors = colors[::-1]

    def is_homogeneous(self) -> bool:
        return len(set(self.colors)) < 2

    def free_space(self) -> int:
        return Vial.capacity - len(self.colors)

    def is_full(self) -> bool:
        return self.free_space() == 0

    def is_empty(self) -> bool:
        return self.free_space() == Vial.capacity

    # return format: (color: str, depth: int)
    def surface(self) -> tuple:
        if self.is_empty():
            return (None, 0)

        color = self.colors[-1]
        depth = 0
        for el in self.colors[::-1]:
            if el == color:
                depth += 1
            else:
                break
        return (color, depth)

    def add(self, color):
        self.colors.append(color)

    def remove(self):
        if not self.is_empty():
            self.colors.pop()

    def __str__(self):
        return str(self.colors)


class Game:
    def __init__(self, vials: list):
        self.vials = []
        self.length = len(vials)
        self.history = []
        for v in vials:
            self.vials.append(Vial(v))

    def get_length(self) -> int:
        return self.length

    def get(self, i: int):
        return self.vials[i]

    def is_solved(self) -> bool:
        return all([v.is_homogeneous() for v in self.vials])

    def show_all(self):
        string = ''
        for i, v in enumerate(self.vials):
            string += str(i + 1) + ' ' + str(v) + '\n'
        return string

    def is_legal_pour(self, orig, dest) -> bool:
        orig = self.get(orig)
        dest = self.get(dest)
        if orig.is_homogeneous() and dest.is_empty():
            return False
        orig_surface = orig.surface()
        dest_surface = dest.surface()
        return ((dest_surface[0] is None) or (orig_surface[0] == dest_surface[0])) \
            and orig_surface[1] <= dest.free_space()

    def pour(self, orig: int, dest: int, undo=False, depth=None):
        orig_obj = self.get(orig)
        dest_obj = self.get(dest)
        colors = (orig_obj.surface()[0], dest_obj.surface()[0])
        orig_surface = orig_obj.surface()
        depth = depth or orig_surface[1]
        if not undo:
            self.history.append((orig, dest, depth))
        for _ in range(depth):
            dest_obj.add(orig_surface[0])
            orig_obj.remove()
        return colors

    def undo(self):
        last_move = self.history.pop()
        self.pour(last_move[1], last_move[0], True, last_move[2])

vials = [
    ['gray', 'y', 's', 'o'],
    ['o', 'gray', 'green', 'r'],
    ['s', 'light blue', 'brown', 'p'],
    ['blue', 'y', 'green', 'r'],
    ['r', 'green', 's', 'light blue'],
    ['y', 'brown', 'light blue', 'p'],
    ['dark green', 'p', 'brown', 'o'],
    ['gray', 'dark green', 'light green', 'blue'],
    ['o', 'light green', 'y', 'brown'],
    ['p', 'blue', 'light blue', 'r'],
    ['blue', 'gray', 'dark green', 's'],
    ['light green', 'light green', 'green', 'dark green'],
    [],
    []
]

game = Game(vials)

def solve(game, instructions: str, inst_num = 1):
    if game.is_solved():
        return 'SOLVED!'
        
    length = game.get_length()
    for i in range(length):
        for j in range(length):
            if i == j:
                continue
            if game.is_legal_pour(i, j):
                # state = game.show_all()
                colors_poured = game.pour(i, j)
                steps = solve(game, instructions, inst_num + 1)
                if steps:
                    return f'{inst_num}. pour {i+1} into {j+1}, from {colors_poured[0]} into {colors_poured[1]} \n' + steps
                game.undo()


print(solve(game, ''))