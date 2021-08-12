import json
import requests

session = None
benchURL = 'http://cml-bench/'

class Simulation:
    def __init__(self):
        self.Name = ''

class Loadcase:
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
    resp = session.get(benchURL + 'rest/simulation/'+str(id))
    obj = json.loads(resp.text)
    s = Simulation()
    s.Name = obj['name']
    s.Owner = obj['owner']
    s.PathNames = obj['pathNames']
    return s

def getLoadcase(id: int):
    global session
    resp = session.get(benchURL + 'rest/loadcase/'+str(id))
    obj = json.loads(resp.text)
    l = Loadcase()
    l.PID = obj['id']
    l.PID2 = obj['id']
    return l

def createsimulation(id: int):
    global session
    l = getLoadcase(id)
    d = {
  "name": "123",
  "description": "",
  "pathNames": None,
  "pid": str(int(l.PID2)+1),
  "allSubmodelsAvailable": True,
  "attachedFilesCount": 0,
  "reference": None,
  "referenceId": None,
  "multivariantId": None,
  "multivariantName": None,
  "dmuId": None,
  "dmuName": None,
  "isInClipboard": None,
  "canRun": None,
  "commentsTotal": 0,
  "flag": None,
  "overview": None,
  "status": None,
  "statusId": None,
  "reportsCount": 0,
  "hasActiveApproval": False,
  "activeApprovalDecision": None,
  "isRemovable": None,
  "userAccess": {},
  "objectType": {
    "name": "simulation",
  },
  "addToClipboard": True
}
    resp = session.post(benchURL + 'rest/simulation', json=d)
