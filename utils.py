#####################################################
# generate simulated data of sequence reads 
#####################################################
import numpy as np
import pymc
import scipy.special as ss

def modelCNV(pos, filename=False):
    profile = np.empty(pos)
    truestate = np.empty(pos)
    current = 0 
    n_rate = 0.1   # normal rate
    h_rate = 0.2   # high rate
    l_rate = 0.05   # low rate
    
    while(current < pos):
        state = np.random.randint(1, 3)  # randomly select state
        prop  = abs(np.random.normal(0, .1, 1))
        lenght = np.random.randint(round(prop*pos))
        if(lenght < 2):
            lenght = 2

        if(state == 1):
            data = np.random.poisson(l_rate, lenght)
        if(state == 2):
            data = np.random.poisson(n_rate, lenght)
        if(state == 3):
            data = np.random.poisson(h_rate, lenght)
            
        end = np.minimum(current+lenght, pos)
        added = end-current
        profile[current:end] = data[0:(added)] #+ noise
        truestate[current:end] = state
        lenght = added
        current += lenght
        
    return profile, truestate


#####################################################
# estimate rate of Poisson distrib from observations
#####################################################
def estimateRate(data, iter=1000):
    rate = pymc.Uniform("rate", lower=0.1, upper=0.4)
    # this also works if you estimate well lower and upper from control
    # DiscreteUniform("rate", lower=1, upper=3) 
    reads = pymc.Poisson('reads', mu=rate, value=data, observed=True)
    M = pymc.Model([reads, rate])
    mcmc = pymc.MCMC(M)
    mcmc.sample(iter, iter/10, verbose=0)
    r_est = mcmc.trace("rate")[:]  
    return np.mean(r_est)
        
def estimateRate_helper(args):
    return estimateRate(*args)



#####################################################
# compute credible region on a vector of reals
#####################################################
def bayes_CR_mu(D, sigma, frac=0.95):
    """Compute the credible region on the mean"""
    Nsigma = np.sqrt(2) * ss.erfinv(frac)
    mu = D.mean()
    sigma_mu = sigma * D.size ** -0.5
    return mu - Nsigma * sigma_mu, mu + Nsigma * sigma_mu
