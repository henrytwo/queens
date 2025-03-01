import random
import queue

class Board:
    def __init__(self, size):
        self.size = size
        self.board = [
            [0 for _ in range(size)]
            for _ in range(size)
        ]

        # Generate the solutions first
        self.solutions = self._generate_solutions()

        # Generate the colored tiles around the solutions
        self._generate_colors()

    def _generate_colors(self):
        # Generate main colors
        for idx, solution in enumerate(self.solutions):
            color = idx + 1
            cell_count = random.randint(1, int(2/3 * self.size ** 2))

            self._fill(color, solution, cell_count)

        # Fill in any remaining holes with nearest adjacent color
        self._fill_holes()

    def _get_neighbours(self, i, j):
        next = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        neighbours = []

        for dx, dy in next:
            nx = i + dx
            ny = j + dy

            if 0 <= nx < self.size and 0 <= ny < self.size:
                neighbours.append((nx, ny))

        return neighbours

    def _fill_holes(self):
        q = queue.Queue()

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    for nx, ny in self._get_neighbours(i, j):
                        color = self.board[nx][ny]
                        if color != 0:
                            q.put((i, j, color))
                            break

        while not q.empty():
            i, j, color = q.get()

            if self.board[i][j] == 0:
                self.board[i][j] = color

                for nx, ny in self._get_neighbours(i, j):
                    q.put((nx, ny, color))


    def _fill(self, color, solution, cell_count):
        q = queue.Queue()

        q.put(solution)
        for _ in range(cell_count):
            if not q.empty():
                i, j = q.get()

                self.board[i][j] = color

                for nx, ny in self._get_neighbours(i, j):
                    if (nx, ny) not in self.solutions and self.board[nx][ny] == 0:
                        q.put((nx, ny))

    def _generate_solutions(self):
        for i in range(1000):
            solution = self._generate_solution()

            if solution:
                return solution
        else:
            raise Exception('Unable to generate board')

    def _generate_solution(self):
        solutions = set()

        available_solutions = set()

        for i in range(self.size):
            for j in range(self.size):
                available_solutions.add((i, j))

        def _select_coordinate():
            if not available_solutions:
                return None

            idx = random.randint(0, len(available_solutions) - 1)

            i, j = list(available_solutions)[idx]

            # Remove the 8 adjacent cells too, in addition to the one we just selected.
            for ni in range(i - 1, i + 2):
                for nj in range(j - 1, j + 2):
                    if (ni, nj) in available_solutions:
                        available_solutions.remove((ni, nj))

            # Remove everything in the same row.
            for nj in range(self.size):
                if (i, nj) in available_solutions:
                    available_solutions.remove((i, nj))

            # Remove everything in th esame column.
            for ni in range(self.size):
                if (ni, j) in available_solutions:
                    available_solutions.remove((ni, j))

            return i, j

        for _ in range(self.size):
            solution = _select_coordinate()

            if solution:
                solutions.add(solution)
            else:
                return None

        return solutions

    def __str__(self):
        out = ''

        for x in range(len(self.board)):
            row_str = ''
            for y in range(len(self.board[0])):
                # Draw white block if this tile is part of the solution
                suffix = '■' if (x, y) in self.solutions else ' '
                value = self.board[x][y] if self.board[x][y] else ' '
                row_str += f'[{suffix}{value:2}{suffix}]'

            if row_str:
                out += row_str + '\n'

        return out

    def __repr__(self):
        return str(self)

if __name__ == '__main__':
    board = Board(10)
    print(board)
    # for i in range(1, 20):
    #     try:
    #         print(i)
    #         board = Board(i)

    #         print(board)
    #     except Exception:
    #         pass