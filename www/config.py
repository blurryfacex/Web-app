from config_default import configs

class Dict(dict):
    def __init__(self,names=(),values=(),**kw):
        super(Dict,self).__init__(**kw)
        for k,v in zip(names,values):
            self[k]=v

    def __getattr__(self,key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r'"Dict" object has no attribute :%s'%key)

    def __setattr__(self,key,value):
        self[key]=value

def merge(default,overwrite):
    d=dict()
    for k,v in default.items():
        if k in overwrite:
            if isinstance(v,dict):
                d[k]=merge(v,overwrite[k])
            else:
                d[k]=overwrite[k]
        else:
            d[k]=v
    return d

def toDict(d):
    D=Dict()
    for k,v in d.items():
        D[k]=toDict(v) if isinstance(v,dict) else v
    return D

try:
    import config_overwrite
    configs=merge(configs,config_overwrite.config)
    print (configs)
except ImportError:
    pass


configs=toDict(configs)
print (configs)