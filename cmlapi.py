import json
import requests

session = None
benchURL = 'http://cml-bench/'

class Simulation:
    def __init__(self):
        self.Name = ''

class StartTask:
    def __init__(self):
        self.sim_id = ''
        self.solver_id = ''
        self.nodes_count = ''
        self.node_cores = ''
    def startSimulation(self):
        global session
        d = {
      "objectType": {
        "name": "task"
      },
      "storyboard": None,
      "storyboardId": None,
      "solverId": str(self.solver_id),
      "solvingType": "Solving",
      "notified": False,
      "autoCreateReport": False,
      "withPostprocessing": False,
      "postprocessorId": None,
      "parentType": {
        "name": "simulation"
      },
      "parentId": str(self.sim_id),
      "customParameters": [
        {
          "name": "nodesCount",
          "value": str(self.nodes_count)
        },
        {
          "name": "autoArguments",
          "value": "true"
        },
        {
          "name": "largeProblem",
          "value": "true"
        },
        {
          "name": "maxCoresOnNode",
          "value": str(self.node_cores)
        },
        {
          "name": "additionalArguments",
          "value": ""
        }
      ]
    }
        resp = session.post(benchURL + 'rest/task', json=d)
        obj = json.loads(resp.text)
        k = Simulation()
        k.taskid = obj['id']
        return k
    
def login(login, password):
    global session
    session = requests.Session()
    d = {'username': login, 'password': password}
    resp = session.post(benchURL + 'rest/login', data=d)
    return resp.status_code == 200


def getSimulation(id: int):
    global session
    resp = session.get('http://cml-bench/rest/simulation/'+str(id))
    obj = json.loads(resp.text)
    s = Simulation()
    s.Name = obj['name']
    s.Owner = obj['owner']
    s.PathNames = obj['pathNames']
    return s