import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
from pylab import *
from sklearn.metrics import roc_curve
from sklearn.model_selection import train_test_split
from numpy.random import choice
from lib.XGBoost_params import *
import lightgbm as lgb

def to_DMatrix(subData):
        """Transform matrix into xgb.DMatrix"""
        X=subData[:,:-1]
        y= np.array(subData[:, -1], dtype=int)
        DMatrix = xgb.DMatrix(X, label=y)
        return DMatrix

def to_DMatrix_LGB(subData):
        """Transform matrix into xgb.DMatrix"""
        X=subData[:,:-1]
        y= np.array(subData[:, -1], dtype=int)
        DMatrix = lgb.Dataset(X, label=y)
        return DMatrix


    
class DataSplitter:
    """ A class for handling splitting and resampling of labeled exampels """
    def __init__(self,data):
        self.data=data
  
    def split_data(self,fraction=0.5):
        """ Split data into two parts randomly
        relative sizes of returned parts are fraction,1-fraction"""
        assert fraction>=0 and fraction <=1
        l=self.data.shape[0]
        C=choice(array(range(l)),int(l*fraction),replace=False)
        selector=array([False for i in range(l)])
        selector[C]=True
        return self.get_subset(selector),\
               self.get_subset(~selector)
        
    def get_subset(self,selection):
        """returns a subset of the rows of data specified by the 
        boolean array selction"""
        assert selection.shape[0]==self.data.shape[0]
        assert selection.dtype==dtype('bool')
        return self.data[selection,:]
   
    def bootstrap_sample(self):
        """ Generate a bootstrap sample from data"""
        l=self.data.shape[0]
        C=choice(array(range(l)),l,replace=True)
        sample=self.data[C,:]
        return sample


def simple_bootstrap(model,Train,Test,param,ensemble_size=2,normalize=True):
    
    
    dtest=to_DMatrix(Test)   # test set is kept fixed
    y_test = array(Test[:,-1],dtype=int8)
    DStrain=DataSplitter(Train)
    log=[]
    for i in range(ensemble_size):  #iterate over randomized training of the classifier        
        boot_train=DStrain.bootstrap_sample()
        if model == 'xgb':
            dtrain = to_DMatrix(boot_train)
            bst,_ = run_xgboost(dtrain,dtest,param)
        elif model == 'lgb':
            dtrain = to_DMatrix_LGB(boot_train)
            bst,_ = run_lgboost(dtrain,dtest,param)
        y_pred = bst.predict(dtest,output_margin=True)
        log.append({
            'i':i,
            'bst':bst,
            'y_pred': y_pred,
            'y_test':y_test
        })
        print('iter %d'%i,end='\r')
    return log

def plot_log(Log):
    """ plots log (evals_result) generated by xgb.train """
    figure(figsize=(12,5))
    i=1
    for loss in ['error','logloss']:
        subplot(1,2,i); i+=1
        for dataset in ['eval','train']:
            _label='%s-%s'%(dataset,loss)
            plot(Log[dataset][loss],label=_label)
        _argmin=argmin(Log['eval'][loss])
        _min=Log['eval'][loss][_argmin]
        _title=f"min of eval-{loss}={_min} at {_argmin}"
        title(_title)
        legend()
        grid()

def run_xgboost(dtrain,dtest,param):
    evallist = [(dtrain, 'train'), (dtest, 'eval')]
    evals_result={}
    num_round=param['num_round']
    cparam=param.copy()
    cparam.pop('num_round')
    
    bst=xgb.train(param_D2L(cparam), dtrain, num_round, evallist,\
                verbose_eval=param['verbose_eval'], evals_result=evals_result, feval = param['custom_metric'])

    return bst,evals_result

def run_lgboost(dtrain,dtest,param):
    evallist = [(dtrain, 'train'), (dtest, 'eval')]
    evals_result={}
    num_round=param['num_round']
    cparam=param.copy()
    cparam.pop('num_round')
    
    bst=lgb.train(param_D2L(cparam), dtrain, num_round, evallist,\
                verbose_eval=False, evals_result=evals_result)

    return bst,evals_result





