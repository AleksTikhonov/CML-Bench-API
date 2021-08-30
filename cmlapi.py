import json
import requests

session = None
benchURL = 'http://cml-bench/'  # URL адрес CML-Bench


class File:
    def __init__(self):
        self.Name = ''


class Stype:
    def __init__(self):
        self.Name = ''


class Submodel:
    def __init__(self):
        self.Name = ''


class Simulation:
    def __init__(self):
        self.Name = ''


class Loadcase:
    def __init__(self):
        self.Name = ''


class Task:
    def __init__(self):
        self.Name = ''


class Solver:
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
    try:
        s.Name = obj['name']
        s.Owner = obj['owner']
        s.PathNames = obj['pathNames']
        s.Status = obj['status']
        s.Full = obj
        s.Error = None
    except KeyError:
        s.Name = s.Owner = s.PathNames = s.Status = s.Full = None
        s.Error = obj['message']
    return s


# Запрос состава субмоделей симуляции
def getSimulationSubmodels(sim_id: int):
    global session
    resp = session.get(benchURL + 'rest/simulation/'+str(sim_id)+'/submodel')
    obj = json.loads(resp.text)
    s = Simulation()
    try:
        s.Submodels = []
        for i in range(len(obj)):
            s.Submodels.append(obj[i]['id'])
        s.Full = obj
        s.Error = None
    except KeyError:
        s.Submodels = s.Full = None
        s.Error = obj['message']
    return s


# Запрос атрибутов лоадкейса
def getLoadcase(lcs_id: int):
    global session
    resp = session.get(benchURL + 'rest/loadcase/'+str(lcs_id))
    obj = json.loads(resp.text)
    try:
        s = Loadcase()
        s.PathID = obj['links'][0]['path'][len(obj['links'][0]['path'])-1]['id']
        s.Name = obj['name']
        s.Owner = obj['owner']
        s.Full = obj
        s.Error = None
    except KeyError:
        s.Name = s.Owner = s.PathID = s.Full = None
        s.Error = obj['message']
    return s


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
    s = Task()
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
    s = Task()
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
    s = Solver()
    s.solver_list = []
    for i in range(len(obj['content'])):
        s.solver_list.append(obj['content'][i]['name'])
    return s


# Возврат имени солвера
def getSolverName(solver_id: int):
    global session
    t = getSolverList()
    s = Solver()
    try:
        s.solver_name = t.solver_list[solver_id-1]
    except IndexError:
        s.solver_name = 'Solver not found'
    return s


# Запрос атрибутов S-type
def getStype(stype_id: int):
    global session
    resp = session.get(benchURL + 'rest/submodelType/'+str(stype_id))
    obj = json.loads(resp.text)
    s = Stype()
    s.PathID = obj['links'][0]['path'][len(obj['links'])]['id']
    s.Name = obj['name']
    s.Owner = obj['owner']
    s.Full = obj
    return s


# Загрузка субмодели
def createSubmodel(stype_id: int, submodel_path: str):
    global session
    f = open(submodel_path)
    l = getStype(stype_id)
    data = {
        "pid": str(l.PathID),
        "addToClipboard": "on"
    }
    files = {
        "file": f
    }
    resp = session.post(benchURL + 'rest/submodel', data=data, files=files)
    obj = json.loads(resp.text)
    s = Submodel()
    s.Full = obj
    try:
        s.submodel_id = obj['duplicates'][0]['createdObject']['id']  # если дубликат субмодели есть
    except IndexError:
        s.submodel_id = obj['set'][0]['id']  # если дубликата субмодели нет
    return s


# Запрос ID файла из симуляции
def getSimulationFileID(sim_id: int, file_name: str, bench_file_path: str):
    global session
    d = {"filters": {"list": [{"name": "path", "value": bench_file_path}]}, "sort": []}
    resp = session.post(benchURL + 'rest/simulation/' + str(sim_id) + '/file/list', json=d)
    obj = json.loads(resp.text)
    s = File()
    for i in range(len(obj['content'])):
        if obj['content'][i]['name'] == file_name:
            s.file_id = obj['content'][i]['id']
            break
        else:
            continue
    return s


# Скачивание файла из симуляции
def downloadSimulationFile(sim_id: int, file_name: str, bench_file_path: str, local_file_path: str):
    global session
    t = getSimulationFileID(sim_id, file_name, bench_file_path)
    resp = session.get(benchURL + 'rest/simulation/' + str(sim_id) + '/file/' + t.file_id + '/export')
    with open(local_file_path + '/' + file_name, "wb") as code:
        code.write(resp.content)
    return resp.status_code == 200


# Запуск субмодели в Remote app
def runRemoteAppSmodel(app_id: str, submodel_id: int):
    global session
    d = {
      "objectTypeName": "remoteApp",
      "details": {
        "application": {
          "id": app_id
        },
        "files": [
          {
            "id": str(submodel_id),
            "objectType": {
              "name": "submodel"
            }
          }
        ],
        "size": {
          "width": 1536,
          "height": 864
        }
      }
    }
    resp = session.post(benchURL + 'rest/job', json=d)
    obj = json.loads(resp.text)
    s = Submodel()
    s.Full = obj
    s.Message = obj['message']
    s.TaskID = obj['value']['id']
    s.StateDisplayName = obj['value']['stateDisplayName']
    s.Status = obj['status']
    return s
