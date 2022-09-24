#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


ipfilename='../input_data/file3.txt'
opfilename='../input_data/file_tst.csv'


# In[3]:


with open(ipfilename) as file_in:
    lines = []
    for line in file_in:
        lines.append(line)


# In[4]:


nlines=len(lines)
#print(nlines)


# In[5]:


## i+314
n_gaszones=24
n_furnace_surfaces=76
n_obstacles=17

i=1 #index of operation time
ntimesteps=0


# In[ ]:


df = pd.DataFrame()
while(i<nlines):

    id_timestep=i-1
    current_line=lines[id_timestep]
    timestep=int(current_line.split()[2][:-1])
    print('timestep:\n',timestep)

    # f: |B| dim vector
    id_frate=(i-1)+3+1
    current_line=lines[id_frate]
    firing_rates=[float(s) for s in current_line.split()]# if s.isdigit()]
    #print('firing_rates:\n',firing_rates,len(firing_rates))

    # s: |B| dim vector:
    id_setpts=id_frate+4
    current_line=lines[id_setpts]
    setpoints=[float(s) for s in current_line.split()]# if s.isdigit()]
    #print('setpoints:\n',setpoints,len(setpoints))

    # F: |G|x12 matrix:
    # |G|=24 by 12 Flow Pattern / Mass balance check for internal boundaries
    id_flowpattern=id_setpts+5

    flowpattern=[]
    for idx in range(n_gaszones):
        current_line=lines[id_flowpattern]
        fptmp=[float(s) for s in current_line.split()]# if s.isdigit()]
        flowpattern.extend(fptmp)
        #print(fptmp,len(fptmp))
        id_flowpattern+=1
    #print('flowpattern:\n',flowpattern,len(flowpattern))

    # Q: |G| dim vector:
    # QENTH (bottom lay QENTH of gas zones 1-12; upper lay QENTH of gas zones 13-24), W:
    id_enthalpy=id_flowpattern+4
    current_line=lines[id_enthalpy]
    q_enthalpy=[float(s) for s in current_line.split()]# if s.isdigit()]
    #print('q_enthalpy:\n',q_enthalpy,len(q_enthalpy))

    # t_G: |G| dim vector Gas zone temperature (C):
    id_tG_gaszone=id_enthalpy+4
    current_line=lines[id_tG_gaszone]
    tG_gaszone=[float(s) for s in current_line.split()]# if s.isdigit()]
    #print('tG_gaszone:\n',tG_gaszone,len(tG_gaszone))

    # t_S(furnace part only): 76 values Updated surface:
    id_tS_furnace=id_tG_gaszone+4
    current_line=lines[id_tS_furnace]
    tS_furnace=[float(s) for s in current_line.split()]# if s.isdigit()]
    #print('tS_furnace:\n',tS_furnace,len(tS_furnace))

    # t_S(obstacle part only) 17x6
    id_tS_obstacle=id_tS_furnace+4

    tS_obstacle=[]
    for idx in range(n_obstacles):
        current_line=lines[id_tS_obstacle]
        tSobstmp=[float(s) for s in current_line.split()]# if s.isdigit()]
        tS_obstacle.extend(tSobstmp)
        #print(tSobstmp,len(tSobstmp))
        id_tS_obstacle+=1
    #print('tS_obstacle:\n',tS_obstacle,len(tS_obstacle))

    # The heat transfer/flux variable w (furnace part only): 76 values
    id_w_flux_furnace=id_tS_obstacle+3
    current_line=lines[id_w_flux_furnace]
    w_flux_furnace=[float(s) for s in current_line.split()]# if s.isdigit()]
    #print('w_flux_furnace:\n',w_flux_furnace,len(w_flux_furnace))

    # The heat transfer/flux variable w (obstacle part only): 17x6
    id_w_flux_obstacle=id_w_flux_furnace+4

    w_flux_obstacle=[]
    for idx in range(n_obstacles):
        current_line=lines[id_w_flux_obstacle]
        wobstmp=[float(s) for s in current_line.split()]# if s.isdigit()]
        w_flux_obstacle.extend(wobstmp)
        #print(wobstmp,len(wobstmp))
        id_w_flux_obstacle+=1
    #print('w_flux_obstacle:\n',w_flux_obstacle,len(w_flux_obstacle))

    # node temperature (furnace) 1D conduction 76x5
    id_nodetmp_1d_furnace=id_w_flux_obstacle+3

    nodetmp_1d_furnace=[]
    for idx in range(n_furnace_surfaces):
        current_line=lines[id_nodetmp_1d_furnace]
        nfurtmp=[float(s) for s in current_line.split()]# if s.isdigit()]
        nodetmp_1d_furnace.extend(nfurtmp)
        #print(nfurtmp,len(nfurtmp))
        id_nodetmp_1d_furnace+=1
    #print('nodetmp_1d_furnace:\n',nodetmp_1d_furnace,len(nodetmp_1d_furnace))

    # node temperature (obstacles) 2D conduction 17x(5x5)
    id_nodetmp_2d_obstacle=id_nodetmp_1d_furnace+4

    nodetmp_2d_obstacle=[]
    for idx in range(n_obstacles):
        tmplist=[]
        for zz in range(5):
            current_line=lines[id_nodetmp_2d_obstacle+zz]
            tmplist.extend([float(s) for s in current_line.split()])
        nodetmp_2d_obstacle.extend(tmplist)
        id_nodetmp_2d_obstacle+=6
    #print('nodetmp_2d_obstacle:\n',nodetmp_2d_obstacle,len(nodetmp_2d_obstacle))

    # Correlation coefficients/ grey gas parameters, b: 2x6 values
    id_corrcoeff_b=id_nodetmp_2d_obstacle+2
    current_line=lines[id_corrcoeff_b]
    corrcoeff_b=[float(s) for s in current_line.split()]# if s.isdigit()]
    id_corrcoeff_b+=1
    current_line=lines[id_corrcoeff_b]
    corrcoeff_b.extend([float(s) for s in current_line.split()])
    #print('corrcoeff_b:\n',corrcoeff_b,len(corrcoeff_b))

    # Convection heat transfer terms (Qconv)i: |G| values
    id_Qconvi=id_corrcoeff_b+4
    current_line=lines[id_Qconvi]
    Qconvi=[float(s) for s in current_line.split()]# if s.isdigit()]
    #print('Qconvi:\n',Qconvi,len(Qconvi))

    # Extinction coefficients kg,n: 1x6
    id_extinctioncoeff_k=id_Qconvi+4
    current_line=lines[id_extinctioncoeff_k]
    extinctioncoeff_k=[float(s) for s in current_line.split()]# if s.isdigit()]
    #print('extinctioncoeff_k:\n',extinctioncoeff_k,len(extinctioncoeff_k))

    # Gas zone Volumes Vi: |G| values
    id_gasvolumes_Vi=id_extinctioncoeff_k+4
    current_line=lines[id_gasvolumes_Vi]
    gasvolumes_Vi=[float(s) for s in current_line.split()]# if s.isdigit()]
    #print('gasvolumes_Vi:\n',gasvolumes_Vi,len(gasvolumes_Vi))

    # Heat release due to input fuel (Qfuel,net)i plus thermal input from air (Qa): |G| values
    id_QfuelQa_sum=id_gasvolumes_Vi+4
    current_line=lines[id_QfuelQa_sum]
    QfuelQa_sum=[float(s) for s in current_line.split()]# if s.isdigit()]
    #print('QfuelQa_sum:\n',QfuelQa_sum,len(QfuelQa_sum))

    ##*****
    # Areas of each surface (furnace+obstacles) Ai: |S| values
    id_surfareas_Ai=id_QfuelQa_sum+4
    current_line=lines[id_surfareas_Ai]
    surfareas_Ai=[float(s) for s in current_line.split()]# if s.isdigit()]
    #print('surfareas_Ai:\n',surfareas_Ai,len(surfareas_Ai))

    # Emissivity of each surface (furnace+obstacles) Epsilon i: |S| values
    id_emissivity_epsi=id_surfareas_Ai+4
    current_line=lines[id_emissivity_epsi]
    emissivity_epsi=[float(s) for s in current_line.split()]# if s.isdigit()]
    #print('emissivity_epsi:\n',emissivity_epsi,len(emissivity_epsi))

    # Heat flux by convection (qconv)i: |S| values
    id_convection_flux_qconvi=id_emissivity_epsi+4
    current_line=lines[id_convection_flux_qconvi]
    convection_flux_qconvi=[float(s) for s in current_line.split()]# if s.isdigit()]
    #print('convection_flux_qconvi:\n',convection_flux_qconvi,len(convection_flux_qconvi))    

    i+=314 # go to next timestep
    
    ntimesteps+=1
    
    df2 = {'timestep':timestep, 'firing_rates':firing_rates, 
           'setpoints':setpoints, 'flowpattern':flowpattern, 
           'q_enthalpy':q_enthalpy, 'tG_gaszone':tG_gaszone,
           'tS_furnace':tS_furnace, 'tS_obstacle':tS_obstacle, 
           'w_flux_furnace':w_flux_furnace, 'w_flux_obstacle':w_flux_obstacle,
           'nodetmp_1d_furnace':nodetmp_1d_furnace, 'nodetmp_2d_obstacle':nodetmp_2d_obstacle, 
           'corrcoeff_b':corrcoeff_b, 'Qconvi':Qconvi, 
           'extinctioncoeff_k':extinctioncoeff_k,'gasvolumes_Vi':gasvolumes_Vi,
           'QfuelQa_sum':QfuelQa_sum, 'surfareas_Ai':surfareas_Ai, 
           'emissivity_epsi':emissivity_epsi,
           'convection_flux_qconvi':convection_flux_qconvi
          }
    df = df.append(df2, ignore_index = True)


print('ntimesteps=',ntimesteps)


# In[ ]:


df.head()


# In[ ]:


print(df.shape)
df.to_csv(opfilename, index=False)

'''
nohup python -u preprocess_data.py > log_f1.txt &
'''