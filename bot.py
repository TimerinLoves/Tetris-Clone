class TetrisBot:
    def __init__(self,grid,shape,x,y):
        self.grid = grid
        self.shape = shape
        self.x = x
        self.y = y

    def find_best_move(self):
        best_score = float('-inf')
        best_rotation = None
        best_x = None
        
        for rotation in self.generate_rotations(self.shape):
            for x in range(len(self.grid[0]) - len(rotation[0]) + 1):
                y = self.get_drop_distance(x)
                if not self.check_collision(rotation, x, y):
                    score = self.calculate_score(rotation, x, y)
                    if score > best_score:
                        best_score = score
                        best_rotation = rotation
                        best_x = x
        return best_rotation, best_x
    
    def generate_rotations(self, shape):
        rotations = [shape]
        rotated_shape = shape
        for _ in range(3):
            rotated_shape = self.rotate_shape(rotated_shape)
            rotations.append(rotated_shape)
        return rotations
    
    def rotate_shape(self,shape):
        return [[shape[j][i] for j in range (len(shape))] for i in range (len(shape[0]))][::-1]

    def get_drop_distance(self, x):
        y = self.y
        while not self.check_collision(self.shape, x, y + 1):
            y += 1
        return y
    
    def calculate_score(self,shape,x,y):
        score = 0

        if self.check_collision(shape,x,y):
            return -float('inf')
        
        simulated_grid = [row[:] for row in self.grid]
        self.place_shape(simulated_grid, shape, x, y)

        for row in simulated_grid[:-4]:
            if all (row):
                score += 100
                score += row.count(0) * 10
        
        for i in range(len(simulated_grid) - 3):
            if all(all(simulated_grid[i + j]) for j in range(4)):
                score += 5000

        return score

    def check_collision(self,shape,x,y):
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] != 0:
                    if (y + i >= len(self.grid) or x + j < 0 or x + j >= len(self.grid[0]) or
                            self.grid[y + i][x + j] != 0):
                        return True
        return False

    def place_shape(self,grid,shape,x,y):
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] != 0:
                    self.grid[y + i][x + j] = shape[i][j]