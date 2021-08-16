import json
import requests

session = None
benchURL = 'http://cml-bench/'  # URL адрес CML-Bench


class Simulation:
    def __init__(self):
        self.Name = ''


class Loadcase:
    def __init__(self):
        self.Name = ''


# Вход в CML-Bench
def login(login, password):
    global session
    session = requests.Session()
    d = {'username': login, 'password': password}
    resp = session.post(benchURL + 'rest/login', data=d)
    return resp.status_code == 200


# Запрос атрибутов симуляции
def getSimulation(sim_id: int):
    global session
    resp = session.get(benchURL + 'rest/simulation/'+str(sim_id))
    obj = json.loads(resp.text)
    s = Simulation()
    s.Name = obj['name']
    s.Owner = obj['owner']
    s.PathNames = obj['pathNames']
    s.Status = obj['status']
    s.Full = obj
    return s


# Запрос состава субмоделей симуляции
def getSimulationSubmodels(sim_id: int):
    global session
    resp = session.get(benchURL + 'rest/simulation/'+str(sim_id)+'/submodel')
    obj = json.loads(resp.text)
    s = Simulation()
    s.Submodels = []
    for i in range(len(obj)):
        s.Submodels.append(obj[i]['id'])
    s.Full = obj
    return s


# Запрос атрибутов лоадкейса
def getLoadcase(lcs_id: int):
    global session
    resp = session.get(benchURL + 'rest/loadcase/'+str(lcs_id))
    obj = json.loads(resp.text)
    l = Loadcase()
    l.PID = obj['id']
    l.PathID = obj['links'][0]['path'][len(obj['links'][0]['path'])-1]['id']
    l.Name = obj['name']
    l.Owner = obj['owner']
    l.Full = obj
    return l


# Создание симуляции
def createSimulation(name: str, lcs_id: int):
    global session
    l = getLoadcase(lcs_id)
    d = {
      "name": name,
      "description": "",
      "pid": l.PathID,
      "referenceId": None,
      "multivariantId": None,
      "dmuId": None,
      "objectType": {
        "name": "simulation",
      },
      "addToClipboard": True
    }
    resp = session.post(benchURL + 'rest/simulation', json=d)
    obj = json.loads(resp.text)
    s = Simulation()
    s.sim_id = obj['id']
    return s


# Добавление субмоделей в симуляцию
def addSubmodel(sub_id: int, sim_id: int):
    global session
    d = getSimulationSubmodels(sim_id)
    if str(sub_id) not in d.Submodels:
        d.Submodels.append(str(sub_id))
    resp = session.post(benchURL + 'rest/simulation/' + str(sim_id) + '/submodel', json=d.Submodels)
    return resp.status_code == 200


# Запуск симуляции на расчет
def startSimulation(sim_id: int, solver_id: int, nodes_count=1, node_cores=1, add_args=""):
    global session
    d = {
      "objectType": {
        "name": "task"
      },
      "storyboard": None,
      "storyboardId": None,
      "solverId": str(solver_id),
      "solvingType": "Solving",
      "notified": False,
      "autoCreateReport": False,
      "withPostprocessing": False,
      "postprocessorId": None,
      "parentType": {
        "name": "simulation"
      },
      "parentId": str(sim_id),
      "customParameters": [
        {
          "name": "nodesCount",
          "value": str(nodes_count)
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
          "value": str(node_cores)
        },
        {
          "name": "additionalArguments",
          "value": str(add_args)
        }
      ]
    }
    resp = session.post(benchURL + 'rest/task', json=d)
    obj = json.loads(resp.text)
    s = Simulation()
    s.task_id = obj['id']
    return s


# Запуск постпроцессинга
def startPostproc(sim_id: int, post_id: int, story_id: int):
    global session
    d = {
      "parentId": str(sim_id),
      "parentType": {
        "name": "simulation",
      },
      "storyboardId": str(story_id),
      "postprocessorId": str(post_id),
      "type": "postprocessing",
    }
    resp = session.post(benchURL + 'rest/task', json=d)
    obj = json.loads(resp.text)
    s = Simulation()
    s.task_id = obj['id']
    return s


# Возврат списка солверов
def getSolverList():
    global session
    d = {
      "filters": {
        "list": []
      },
      "sort": [
        {
          "direction": "ASC",
          "field": "name"
        }
      ]
    }
    resp = session.post(benchURL + 'rest/solver/list', json=d)
    obj = json.loads(resp.text)
    s = Simulation()
    s.solver_list = []
    for i in range(len(obj['content'])):
        s.solver_list.append(obj['content'][i]['name'])
    return s


# Возврат имени солвера
def getSolverName(solver_id=1):
    t = getSolverList()
    s = Simulation()
    try:
        s.solver_name = t.solver_list[solver_id-1]
    except IndexError:
        s.solver_name = 'Solver not found'
    return s
