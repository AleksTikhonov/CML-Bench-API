import cmlapi

b = cmlapi.login('atikhonov', '1-,Yh1[Y')

if b:
    #task = cmlapi.getSimulationSubmodels(924369)
    #print(task.Test)
    #task = cmlapi.createsimulation('123',885339)
    #print(task.simulationid)
    #l1 = cmlapi.getLoadcase(885339)
    #print(l1.PathID)
    #cmlapi.addSubmodel(926800,924369)
    #task = cmlapi.startPostproc(924369, 92, 951777)
    #print(task.task_id)
    task = cmlapi.getSolverList()
    print(task.Full)