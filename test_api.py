import cmlapi

b = cmlapi.login('atikhonov', '1-,Yh1[Y')

if b:
    #t = cmlapi.StartTask()
    #t.sim_id = 924369
    #t.solver_id = 10
    #t.nodes_count = 5
    #t.node_cores = 23
    #task = t.startSimulation()
    #print(task.taskid)
    cmlapi.createsimulation(885339)
    #l1 = cmlapi.getLoadcase(885339)
    #print(l1.PID)