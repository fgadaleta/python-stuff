#!/usr/bin/python

#########################################################################
## bayesCBS                       
## A software to detect CNV from case-control CN profiles  
## usage: ./bayesCBS.py  
## Copyright 2015 Francesco Gadaleta - UZLeuven
##########################################################################

import pymc as pm 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as signal
import cPickle
import multiprocessing as mp 
import os, sys, getopt, time
import utils

#np.random.seed(1370)
def main(argv):
        print "Generating simulated data..."
	control, state = utils.modelCNV(5000, False)
	case = np.copy(control)
        
        # 1000-loc deletion 
        case[1500:2500] = control[1500:2500]-1
        idx = np.where(case < 0)
        case[idx] = 0
        # 500-loc deletion 
        case[2700:3200] = control[2700:3200]-1
        idx = np.where(case < 0)
        case[idx] = 0
        # 80-loc duplication at 327 and 4000
        case[327:408] = control[327:408]+1
        case[4000:4500] = control[4000:4500]+1

        
        ## generate seqCBS-friendly file 
        idx = np.where(control>0)[0]
        readstart = [] 
        
        for i in idx:
                times = int(control[i])
                for j in range(times):
                        readstart.append(i)
            
        with open("data/seqCBS_control.txt",'w') as f:
                f.write("\n".join(map(str,readstart)))
        f.close()

        idx = np.where(case>0)[0]
        readstart = [] 

        for i in idx:
                times = int(case[i])
                for j in range(times):
                        readstart.append(i)
                
                with open("data/seqCBS_case.txt",'w') as f:
                        f.write("\n".join(map(str,readstart)))
                f.close()
                
                
        ################################
        numpos = len(case)
        print "Generated %d positions of noisy CNV" %(numpos)
        
        fig = plt.figure()
        ax = fig.add_subplot(611)
        p = ax.plot(control, 'bo', markersize=2)
        ax.set_xlabel('genomic positions')
        ax.set_ylabel('reads')
        ax.set_title('Simulated control CN profile')
        
        ax = fig.add_subplot(612)
        p = ax.plot(case, 'ro', markersize=2)
        ax.set_xlabel('genomic positions')
        ax.set_ylabel('reads')
        ax.set_title('Simulated case CN profile')
        
        ax = fig.add_subplot(613)
        ax.plot(state, 'ro', markersize=2)
        ax.set_xlabel('genomic positions')
        ax.set_ylabel('true rate')
        ax.set_title('True rate of simulated case CN profile')

        fig.show()

        start=time.time() 
        
        dels = []
        dups = [] 
        
        deletion = 0
        duplication = 0
        sliding = 1000
        sliding_slack = 0.8*sliding
        
        pool = mp.Pool(processes=4)
        
        chunksize = 5000
        chunks = np.round(len(control)/chunksize)
        case_data_chunks  = np.split(case, chunks)
        contr_data_chunks = np.split(control, chunks)

        # TODO
        slack = 100 # how tolerant are we for consecutive events
        mindist = 0  # minimum distance between normal rates (after a while del/dup counts should reset)

        control_rates = np.empty(len(control)-sliding)
        case_rates = np.empty(len(case)-sliding)
        diff_rates = np.empty(len(case)-sliding)


        for i in range(len(control)-sliding):
                winstart = i
                winend = i+sliding
                
                contr_data = control[winstart:winend]
                case_data = case[winstart:winend]
                size = len(contr_data)

                #result = pool.map(estimateRate, [contr_data, case_data])
                params = [(contr_data, sliding), (case_data, sliding)]
                result = pool.map(utils.estimateRate_helper, params)
                controlRate = result[0]   # rate of control window 
                caseRate = result[1]      # rate of case window 
                
                control_rates[i] = controlRate
                case_rates[i] = caseRate
                diff_rates[i] = controlRate-caseRate
                discrepancy = diff_rates[i] 
                
                ##ax = fig.add_subplot(414)
                #if np.abs(diff_rates[i]) < .0005:
                #print "discrepancy %f duplication %d deletion %d" % (discrepancy,duplication,deletion)
    
                if(discrepancy<0):
                        duplication = duplication + 1
                        if deletion>0:
                                deletion-=1
                        if(duplication > sliding_slack):
                                dups.append([i, discrepancy]) # TODO not sure   
                                print "detected duplication at position [%d-%d]" % (i-duplication, i-duplication+size)
                                ##plt.axvline(i, linestyle='--')
                                duplication = 0
                                deletion = 0

                elif(discrepancy>0):
                        deletion = deletion+1
        
                        if duplication>0:
                                duplication-=1
                
                        if(deletion > sliding_slack):
                                dels.append([i,discrepancy])   # Work in progress 
                                #dels = np.hstack((dels, i+sliding))   # Work in progress 
                                print "detected deletion at position [%d-%d]" % (i-deletion, i-deletion+size)
                                ##plt.axvline(i, linestyle='--')
                                deletion = 0
                                duplication = 0
    
                # if very small discrepancy set back the triggers
                if np.abs(discrepancy)<.001:
                        if duplication >0:
                                duplication-=1
                        if deletion>0:
                                deletion-=1
                                
                
        ## plotting around 
        # ax.plot(control_rates, 'ro', markersize=3)
        # ax.plot(i, caseRate, 'ro', markersize=3)
        # ax.plot(i, controlRate, 'bo', markersize=2)
        # ax.set_xlabel('genomic positions')
        # ax.set_ylabel('est. rate')
        # plt.draw()
        # fig.show()
        
        ax = fig.add_subplot(614)
        ax.plot(control_rates, 'bo', markersize=2)
        ax.plot(case_rates, 'ro', markersize=3)
        ax.set_xlabel('genomic positions')
        ax.set_ylabel('est. rate')
        
        ax = fig.add_subplot(615)
        #ax.plot(np.log(np.abs(diff_rates)), 'bo', markersize=3)
        ax.plot(diff_rates, 'bo', markersize=3)
        ax.set_xlabel('genomic positions')
        ax.set_ylabel('diff est. rate')

        #ax = fig.add_subplot(616)
        #ax.plot(1-np.exp(-np.abs(diff_rates)), 'bo', markersize=3)
        #ax.set_xlabel('genomic positions')
        #ax.set_ylabel('prob(case != control)')
        plt.draw()
        end=time.time()
        
        # print("[{0:.0f}, {1:.0f}]".format(*utils.bayes_CR_mu(diff_rates[600:1200], 5, frac=0.70)))
        print utils.bayes_CR_mu(diff_rates[0:450], .1, frac=0.90)
        print utils.bayes_CR_mu(diff_rates[1500-2500], .1, frac=0.90)
        print utils.bayes_CR_mu(diff_rates[600:1200], .1, frac=0.90)
        print utils.bayes_CR_mu(diff_rates[3500:4500], .1, frac=0.90)
        

        print "Finished in %f secs!" % (end-start)
        print "Detected deletions"
        print dels
        print "Detected duplications"
        print dups
        plt.show()
        
        # write to file
        print "Writing results to file"
        np.savetxt("control.dat", control, delimiter=",")
        np.savetxt("case.dat", case, delimiter=",")
        np.savetxt("control_rates.dat", control_rates, delimiter=",")
        np.savetxt("case_rates.dat", case_rates, delimiter=",")
        np.savetxt("diff_rates.dat", diff_rates, delimiter=",")



if __name__ == "__main__":
        main(sys.argv[1:])
