import sys
import time

from screen_controller import ScreenController


class HanoiTower:
    def __init__(self, disk_nums, speed):
        self.disk_nums = disk_nums
        self.speed = speed
        self.steps = 0
        self.init_disk()
        self.init_graph()
        self.sc = ScreenController()

    def start(self):
        self.sc.hide_cursor()
        self.sc.clear()
        self.draw()
        self.solve(self.disk_nums, self.rods[0], self.rods[1], self.rods[2])
        self.slide()
        self.sc.show_cursor()

    def slide(self):
        width = self.disk_nums * 6 - 3 - 3
        
        for i in range(width):
            print('%s%s%s' % (' ' * i, 'Done!', ' ' * (width-i)), end='\r')
            time.sleep(0.05)
        
        for i in range(width):
            print('%s%s%s' % (' ' * (width-i), 'Done!', ' ' * i), end='\r')
            time.sleep(0.05)
        
        print('Done!  ')
        print('\n')
    
    def init_disk(self):
        self.rods = [
            [n + 1 for n in reversed(range(self.disk_nums))],
            [], []
        ]
    
    def init_graph(self):
        n = self.disk_nums
        self.d = [' ' * (n-1) + '|' + ' ' * (n-1)]
        for i in range(n):
            i += 1
            ss = ' ' * (n-i)
            ss += '-' * ((i-1) if i > 0 else 0)
            ss += '+'
            ss += '-' * ((i-1) if i > 0 else 0)
            ss += ' ' * (n-i)
            self.d.append(ss)

    def solve(self, n, m, a, t):
        if n == 1:
            t.append(m[-1])
            del m[-1]
            self.draw()
        else:
            self.solve(n-1, m, t, a)
            self.solve(1, m, a, t)
            self.solve(n-1, a, m, t)

    def draw(self):
        total = self.disk_nums
        self.sc.move(0, 0)
        print('Step %d' % self.steps)
        self.steps += 1
        graph_str = self.d[0] * 3 + '\n'
        graph = [[0 for _ in range(total)] for _ in range(3)]
        for i, rod in enumerate(self.rods):
            for j, disk in enumerate(rod):
                graph[i][j] = disk
        for i in range(total):
            for j in range(3):
                graph_str += self.d[graph[j][total-1-i]]
            graph_str += '\n'
        print(graph_str)
        time.sleep(self.speed)

if __name__ == '__main__':
    disk_num = 3
    ani_speed = 0.5
    argc = len(sys.argv)
    if argc > 1:
        try:
            disk_num = int(sys.argv[1])
            if disk_num < 1:
                raise ValueError()
        except:
            disk_num = 3
            print('Warning: First argument must be integer.')
            time.sleep(1)
    if argc > 2:
        try:
            ani_speed = float(sys.argv[2])
            if ani_speed < 0:
                raise ValueError()
        except:
            ani_speed = 0.5
            print('Warning: Second argument must be float.')
            time.sleep(1)
    ht = HanoiTower(disk_num, ani_speed)
    ht.start()
