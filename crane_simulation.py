# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 10:36:21 2020

@author: User
"""

import numpy as np
import subprocess
from sys import platform
import os
import csv

cwd = os.getcwd()
#print(cwd)
  
#PATH TO ABAQUS TEMP FILE
if platform == "linux" or platform == "linux2":
    # Linux
    abaqusPath = '/opt/abaqus611/Commands/abaqus'
    tmp = '/tmp/'
elif platform == "darwin":
    # OS X
    pass
elif platform == "win32":
    # Windows...
    abaqusPath = 'C:\\SIMULIA\\Abaqus\\6.14-5\\code\\bin\\abq6145.exe' 
    tmp = 'C:/Temp/' 

#FUNCTION TO DELETE FILES
def remove():
    for case in 'case1 case2'.split():
        for ext in 'sta com msg prt dat inp lck sim ipm log rep'.split():
            if os.path.exists(f'{tmp}/{case}.{ext}'):
                os.remove(f'{tmp}/{case}.{ext}') 
remove()

#ALLOWABLE STRESS
granica_razvlačenja = 250e6 #Pa
faktor_sigurnosti = 1.5
sigma_allowable = granica_razvlačenja/faktor_sigurnosti
#print('sigma_allowable: ',sigma_allowable/1e6, 'MPa')

#OPTIMIZATION VARIABLE VECTORS
def opt_func(a, h, b, t, r):
    
    # CASE1 - FINDING VALUES OF I - BEAM / CIRCULAR BEAM
    with open('case1_tamplet.inp', 'r') as f:
        content = f.readlines()
    for i in range(len(content)):
        if content[i].strip() == '** Section: I_greda  Profile: I_profil':
            content[i+2] ='0.' + ',' +str(h) + ',' + str(b) + ',' + str(b) + ',' + str(t) + ',' + str(t) + ',' + str(t) + ',' + '\n'
        if content[i].strip() == '** Section: O_greda  Profile: O_profil':
            content[i+2] = str(r) + '\n'
            
            
    #CASE1 - FINDING VALUES TO CHANGE CRANE WIDTH     
    nodes1 = np.array([content[row].split(',') for row in range(17,592)])
    nodes1[:,2] = [str(a * float(koord1)) for koord1 in nodes1[:,2]]
    content[17:592] = [','.join(row) for row in nodes1.tolist()]
        
        
        
    #CASE1 - WRITING NEW VALUES TO case1.inp   
    with open(f'{tmp}/case1.inp', 'w') as f:
        f.writelines(content)
                     
    # CASE2 - FINDING VALUES OF I - BEAM / CIRCULAR BEAM
    with open('case2_tamplet.inp', 'r') as f:
        content = f.readlines()
    for i in range(len(content)):
        if content[i].strip() == '** Section: I_greda  Profile: I_profil':
            content[i+2] ='0.' + ',' +str(h) + ',' + str(b) + ',' + str(b) + ',' + str(t) + ',' + str(t) + ',' + str(t) + ',' + '\n'
        if content[i].strip() == '** Section: O_greda  Profile: O_profil':
            content[i+2] = str(r) + '\n'
            
    #case2 - FINDING VALUES TO CHANGE CRANE WIDTH       
    nodes2 = np.array([content[row].split(',') for row in range(17,592)])
    nodes2[:,2] = [str(a * float(koord2)) for koord2 in nodes2[:,2]]
    content[17:592] = [','.join(row) for row in nodes2.tolist()]
        
    #CASE1 - WRITING NEW VALUES TO case2.inp
    with open(f'{tmp}/case2.inp', 'w') as f:
        f.writelines(content)
         
    #STARTING ABAQUS SIMULATION FOR CASE 1
    p = subprocess.Popen([abaqusPath, 
                  'input=case1.inp',
                  'job=case1',
                  #'cpus=4',
                  'interactive'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=tmp)
    out, err = p.communicate() 
    #print(out)
    
    #GENERATING REPORT FILE FROM ODB FILE FOR CASE 1
    p = subprocess.Popen([abaqusPath,
                'odbreport',
                'odb=case1', 
                'job=case1', 
                'frame=_LAST_',
                'step=_LAST_',
                'field=misessMAX', 
                'instance=CRANE-1', 
                #'invariant',
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=tmp)
    out, err = p.communicate()  
    
    #READING STRESS VALUES FROM THE REPORT FILE FOR CASE 1
    misess_stress1 = np.genfromtxt(f'{tmp}/case1.rep',skip_header=50, skip_footer=4, usecols=(3, ))
    misess_max1 = np.max(misess_stress1)
    print('Sigma_max1: ', misess_max1/1e6, 'MPa')
    
    #STARTING ABAQUS SIMULATION FOR CASE 2
    p = subprocess.Popen([abaqusPath, 
                  'input=case2.inp',
                  'job=case2',
                  #'cpus=4',
                  'interactive'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=tmp)
    out, err = p.communicate() 
    #print(out)
    
    #GENERATING REPORT FILE FROM ODB FILE FOR CASE 2
    p = subprocess.Popen([abaqusPath,
                'odbreport',
                'odb=case2', 
                'job=case2', 
                'frame=_LAST_',
                'step=_LAST_',
                'field=misessMAX', 
                'instance=CRANE-1', 
                #'invariant',
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=tmp)
    out, err = p.communicate()  
    
    #READING STRESS VALUES FROM THE REPORT FILE FOR CASE 2
    misess_stress2 = np.genfromtxt(f'{tmp}/case2.rep',skip_header=50, skip_footer=4, usecols=(3, ))
    misess_max2 = np.max(misess_stress2)
    print('Sigma_max2: ', misess_max2/1e6, 'MPa')
    
    
    #READING MASS VALUES FROM .DAT FILE 
    with open('case1.dat', 'r') as m:      
        mass_content1 = m.readlines()
        m.close()
        
        for i in range(len(mass_content1)):
            if mass_content1[i] == '                    TOTAL MASS OF MODEL\n':
                for j in range(3):
                    mass1 = float(mass_content1[i+2])
                    print('mass: ', mass1, 'kg')
                    break

    #GOAL FUNCTION
    return mass1, misess_max1 - sigma_allowable, misess_max2 - sigma_allowable

a, h, b, t, r = 1, 0.04138, 0.05, 0.005, 0.01
opt_func(a, h, b, t, r)

remove()


    