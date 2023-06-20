"""Robot."""
from copy import deepcopy
from algorithm import AStar
from config import config
from simpy.rt import RealtimeEnvironment
class Sensor:
    """Capteur."""
    def __init__(self, env, robot) -> None:
        """Création du/des capteur(s)."""
        self.environment = env
        self.robot = robot

    def observe_environment(self):
        """Récupère les données d'environnement."""
        self.robot.grille = deepcopy(self.environment.grid)
        self.robot.position = deepcopy(self.environment.position_robot)

class Effector:
    """Action sur l'environnement."""
    def __init__(self, env, robot) -> None:
        """Création de l'effecteur."""
        self.environment = env
        self.robot = robot

    def move(self, dx, dy):
        """Déplace le robot."""
        self.environment.move_robot(dx, dy)
        self.robot.perf.stats["path"] += "("+str(dx)+","+str(dy)+")"
        self.robot.perf.stats["energy_consumed"] += 1

    def deliver(self, x, y):
        """Aspire une pousière."""
        self.robot.perf.stats["energy_consumed"] += 1

        if self.environment.grid["table"][x][y]:
            self.environment.unset_objet("table", x, y)
            self.robot.perf.stats["tables_delivered"] += 1
    def stay_put(self): 
        """Don't do anything."""


    def execute(self):
        """Execute l'action dans la liste."""
        try:
            action = self.robot.actions.pop(0)

            if action[0] == "table":
                x, y = action[1]
                self.deliver(x, y)

            elif action[0] == "move":
                dx, dy = action[1]
                dx=self.robot.position["x"] + dx
                dy=self.robot.position["y"] + dy
                self.move(dx, dy)
        except IndexError:
            self.stay_put()
        finally:
            self.environment.update_stats()

        return len(self.robot.actions) > 0
class Robot:
    """Agent intelligent."""


    def __init__(self, env, stats) -> None:
        """Création du robot."""
        self.rte = RealtimeEnvironment(factor=config["speed_simu"])
        self.rte.process(self.robot_event())
        # Capteur(s)
        self.capteur = Sensor(env, self)
        # Algo de Recherche
        self.algo = AStar(self)
        # Actionneur(s)
        self.actionneur = Effector(env, self)

        self.has_strategy = False
        self.grille = []
        self.position = {}
        self.actions = []
        self.perf = stats

    def run(self):
        self.rte.run()
    def robot_event(self):
        """Robot mainloop."""
        iteration = 0
        refresh_rate = config["size"]["width"] + config["size"]["heigh"] - 1
        while True:
            yield self.rte.timeout(1)
            iteration += 1
            # Sensor
            self.capteur.observe_environment()
            # Modifier l'état
            if not (any(any(x) for x in self.grille["table"])):
                self.actionneur.execute()
                continue
            # choose action
            if (iteration % refresh_rate == 0) | (not self.has_strategy):
                self.algo.search()
                self.has_strategy = True
            # Effectuer l'action
            self.has_strategy = self.actionneur.execute()

