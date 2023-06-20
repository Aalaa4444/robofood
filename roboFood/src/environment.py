"""Environment."""
from threading import Thread
from board import Board
from config import config
from events import Events
from robot import Robot
from statistique import Stats
class Environment:
    def __init__(self, line, col, x,y, goal) -> None:
        self.line = line
        self.col = col
        self.goal=goal
        self.grid = {
            "table": [[False for y in range(self.line)] for x in range(self.col)],
        }
        # initial robot
        self.position_robot = {
            "x": x,
            "y": y,
        }
        ##### Stats #####
        stats = Stats(x,y)
        thread_stats = Thread(target=stats.run)
        thread_stats.daemon = True
        thread_stats.start()

        ##### GUI #####
        self.board = Board(self, stats,x, y)

        #for objet in [""]:self.set_objet(objet, randint(0, self.col - 1), randint(0, self.line - 1))

        self.set_objet("robot", self.position_robot["x"], self.position_robot["y"])

        ##### Event #####
        events = Events(self)
        thread_event = Thread(target=events.run)
        thread_event.daemon = True
        thread_event.start()

        ##### Robot #####
        robot = Robot(self, stats)
        thread_robot = Thread(target=robot.run)
        thread_robot.daemon = True
        thread_robot.start()

        self.board.display()

    def set_objet(self, objet, x, y):
        if objet != "robot":
            self.grid[objet][x][y] = True

        self.board.display_objet(x, y, objet)

    def unset_objet(self, objet, x, y):
        self.grid[objet][x][y] = False

        self.board.hide_objet(objet, self.position_robot["x"], self.position_robot["y"])

    def move_robot(self, dx, dy):
        self.board.hide_objet(
            "robot", self.position_robot["x"], self.position_robot["y"]
        )
        self.position_robot["x"] = dx
        self.position_robot["y"] = dy
        self.board.display_objet(
            self.position_robot["x"], self.position_robot["y"], "robot"
        )

    def update_stats(self):
        self.board.update_stats()

'''def main():
    size = config["size"]
    Environment(size["width"], size["heigh"])
if __name__ == "__main__":
    main()'''
