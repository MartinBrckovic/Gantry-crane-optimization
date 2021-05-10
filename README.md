The goal of the project is to reduce the mass of the crane by optimizing beam profile dimensions and crane width. The restriction of the optimization is that the Von Misses stresses must be lower the the allowed stresses.

There are two cases of loading. Case 1 is with two symmetrical forces ( each  25kN ) and the second case is with one force on one side of the crane ( 50kN ). The inital simulation was made in Abaqus. The input files were ( case1_tamplet.inp, case2_tamlpet.inp ) used as a start point for the optimization. The python script "crane_simulation.py" is a python script where we have defined the goal function. For the optimization we are using Nomad Blackbox optimization softwere. "nomad_crane.txt" is an txt file where we have defined our optimization. The python script "opt.py" unites the two files described before. The optimization reasult are showed by running the "post-processing.by" script. 