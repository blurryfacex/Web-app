import logging
import aiomysql


__author__='llx'

def log(sql,args=()):
    logging.info('sql:%s'%sql)

async def create_pool(loop,**kw):
    logging.info('create database connection pool...')
    global __pool
    __pool=await aiomysql.create_pool(
        host=kw.get('host','localhost'),
        port=kw.get('port',8989),
        user=kw.get('user','root'),
        password=kw.get('password',123456),
        db=kw['db'],
        charset=kw.get('charset','utf8mb4'),
        autocommit=kw.get('autocommit',True),
        maxsize=kw.get('maxsize',10),
        minsize=kw.get('minsize',1),
        loop=loop
    )

async def select(sql,args,size=None):
    log(sql,args)
    global __pool
    with (await __pool) as conn:
        cur=await conn.sursor(aiomysql.DictCursor)
        await cur.execute(sql.replace('?','%s'),args or ())
        if size:
            rs=await cur.fetchmany(size)
        else:
            rs=await cur.fetchall()
        await cur.close()
        logging.info('rows returned:%s' %len(rs))
        return rs


async def execute(sql,args):
    log(sql,args)
    global __pool
    with (await __pool) as conn:
        try:
            cur=await conn.cursor()
            await cur.execute(sql.replace('?','%s'),args)
            affected=cur.rowcount
            await cur.close()
        except BaseException as e:
            raise
        return affected

def create_args_strings(num):
    n=[]
    for i in range(num):
        n.append('?')
    return  ','.join(n)

class Field(object):
    def __init__(self,name,column_type,primary_key,default):
        self.name=name
        self.column_type=column_type
        self.primary_key=primary_key
        self.default=default

    def __str__(self):
        return "<%s,%s:%s>" %(self.__class__.__name__,self.name,self.column_type)

class StringField(Field):
    def __init__(self,name=None,primary_key=None,default=None,ddl='varchar(100)'):
        super().__init__(name,ddl,primary_key,default)

class BooleanField(Field):
    def __init__(self,name=None,default=False):
        super().__init__(name,'boolean',False,default)

class IntergerField(Field):
    def __init__(self,name=None,primary_key=False,default=0):
        super().__init__(name,'bigint',primary_key,default)

class FloatField(Field):
    def __init__(self,name,primary_key=False,default=0.0):
        super().__init__(name,'real',primary_key,default)

class TextField(Field):
    def __init__(self,name=None,default=None):
        super().__init__(name,'text',False,default)


class ModelMetaClass(type):
    def __new__(cls,name,bases,attrs):
        if name=='Model':
            return type.__new__(cls,name,bases,attrs)
        tablename=attrs.get('__table__',None) or name
        logging.info('found model:%s (table:%s)' %(name,tablename))
        mapping={}
        fields=[]
        primaryKey=None

        for k,v in attrs.items():
            if isinstance(v,Field):
                logging.info('found mapping:%s==>%s' %(k,v))
                mapping[k]=v
                if v.primary_key:
                    if primaryKey:
                        raise RuntimeError('Duplicate primary key for field %s' %k)
                    primaryKey=k
                else:
                    fields.append(k)

        if not primaryKey:
            raise RuntimeError("can't found primary key")

        for k in mapping.keys():
            attrs.pop(k)

        escaped_fields=list(map(lambda f:"'%s'" %f,fields))
        attrs['__mappings__']=mapping
        attrs['__table__']=tablename
        attrs['__fields__']=fields
        attrs['__primarykey__']=primaryKey

        attrs['__select__']="select '%s',%s from '%s'" %(primaryKey,','.join(escaped_fields),tablename)
        attrs['__insert__']="insert into '%s' (%s,'%s') values (%s)" %(tablename,','.join(escaped_fields),primaryKey,create_args_strings(len(escaped_fields)+1))
        attrs['__delete__']="delete from '%s' where '%s'=?" %(tablename,primaryKey)
        attrs['__update__']="update '%s' set %s where '%s'=?" %(tablename,','.join(map(lambda f:"'%s'" %f,fields)),primaryKey)
        return type.__new__(cls,name,bases,attrs)


class Model(dict,metaclass=ModelMetaClass):

    def __init__(self,**kw):
        super().__init__(**kw)

    def __getattr__(self,key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' attribute has no attribute '%s'" %key)

    def __setattr__(self,key,value):
        self[key]=value

    def getValue(self,key):
        return getattr(self,key,None)

    def getValueOrDefault(self,key):
        value=self.getValue(key)
        if value is None:
            field=self.__mapppings__[key]
            if field.default is not None:
                value=field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s:%s' %(key,str(value)))
                setattr(self,key,value)
        return value

    @classmethod
    async def find(cls,pk):
        'find object by primary key'
        rs=await select("%s where '%s'=?" %(cls.__select__,cls.__primary_key__),[pk],1)
        if len(rs)==0:
            return None
        return cls(**rs[0])

    @classmethod
    async def findNumber(cls,selectField,where=None,args=None):
        'find number by select and where'
        sql=["select %s _num_ from '%s'" %(selectField,cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs=await select(' '.join(sql),args,1)
        if len(rs)==0:
            return None
        return rs[0]['_num_']

    @classmethod
    async def findall(cls,where=None,args=None,**kw):
        'find objects by where claues'
        sql=[cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args=[]

        orderBy=kw.get('orderBy',None)
        if orderBy:
            sql.append('order By')
            sql.append(orderBy)

        limit=kw.get('limit',None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit,int):
                sql.append('?')
                sql.append(limit)
            elif isinstance(limit,tuple) and len(limit)==2:
                sql.append('?,?')
                sql.append(limit)
            else:
                raise ValueError('Invalid limit value:%s'%str(limit))
        rs=await select(' '.join(sql),args)
        return [cls(**r) for r in rs]

    async def save(self):
        args=list(map(self.getValueOrDefault,self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows=await execute(self.__insert__,args)
        if rows !=1:
            logging.warn('faild to insert record affected rows %s' %rows)

    async def update(self):
        args=list(map(self.getValue,self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows=await execute(self.__update__,args)
        if rows !=1:
            logging.warn('faild to update to primary ke:affected rows %s'%rows)

    async def remove(self):
        args=[self.getValue(self.__primary_key__)]
        rows=await execute(self.__delete__,args)
        if rows !=1:
            logging.warn('failed to remove by primary key: affected rows %s'%rows)