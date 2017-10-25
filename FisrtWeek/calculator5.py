#!/usr/bin/env python3
import queue
import sys
from multiprocessing import Process,Queue
import getopt
import configparser



q_user = Queue()
q_result = Queue()



class Config(object):
    def __init__(self,configfile,cityname):
        self._configfile = configfile
        self._configdict = {} 
        self._cityname = cityname
  
    def readConfig(self):
        config = configparser.ConfigParser()
        config.read(self._configfile)
        tmpCityname = self._cityname.upper()
        self._configdict = config[tmpCityname]
        return self._configdict   
            
class UserData(Process):

    def __init__(self,userfile):
        self._userfile = userfile
    
    def run(self):
        userdict = {}
        with open('{0}'.format(self._userfile)) as ufile:
            for tmpline in ufile:
                tmpstr = tmpline.split(',')
                userdict[int(tmpstr[0].strip())]=int(tmpstr[1].strip())
            q_user.put(userdict)



class CalcuResult(Process):

    def __init__(self,configdict):
        self._configdict = configdict

    def calShebao(self,salary):
        
        tmp=salary
        if salary < float(self._configdict['jishul']):
            tmp = float(self._configdict['jishul'])
        elif salary > float(self._configdict['jishuh']):
            tmp = float(self._configdict['jishuh'])

        sheBao = tmp*(float(self._configdict['yanglao']) + float(self._configdict['yiliao']) + float(self._configdict['shiye']) + float(self._configdict['gongshang']) + float(self._configdict['shengyu']) + float(self._configdict['gongjijin']))
        return sheBao

   
    def calTax(self,salary,sbMoney):
        try:
            
            taxMoney = salary - sbMoney -3500
            finalTax = 0.00
            if (salary-sbMoney) <= 3500:
                finalTax = 0.00          
            elif taxMoney <=1500:
                finalTax = taxMoney * 0.03 - 0    
            
            elif taxMoney <=4500: 
                finalTax = taxMoney * 0.1 - 105        

            elif taxMoney <=9000: 
                finalTax = taxMoney * 0.2 - 555        

            elif taxMoney <=35000: 
                finalTax = taxMoney * 0.25 - 1005        

            elif taxMoney <=55000: 
                finalTax = taxMoney * 0.3 - 2755        

            elif taxMoney <=80000: 
                finalTax = taxMoney * 0.35 - 5505        

            else: 
                finalTax = taxMoney * 0.45 - 13505        

        except ValueError:
            print("Parameter Error")

        finally:
            return finalTax

    def run(self):
        while True:
            try:
                udata = q_user.get(timeout=1)
            except queue.Empty:
                return
            data = []
            for tmpdata in udata.items():
                sbMoney = self.calShebao(tmpdata[1])
                taxMoney= self.calTax(tmpdata[1],sbMoney)
                shifa = tmpdata[1] - sbMoney - taxMoney
                
                tmpLine = '{0},{1},{2:.2f},{3:.2f},{4:.2f}\n'.format(tmpdata[0],tmpdata[1],sbMoney,taxMoney,shifa)
                data.append(tmpLine)
            q_result.put(data)

class WriteResult(Process):

    def __init__(self,outputfile):
        self._outputfile = outputfile 

    def run(self):
        while True:
            try:         
                result = q_result.get(timeout=1)
            except queue.Empty:
                return
            result.sort()   
            with open('{0}'.format(self._outputfile),'w') as ofile:
                for tmpLine in result:
                    ofile.write(tmpLine)


if __name__ == "__main__":

    try:
        options,args = getopt.getopt(sys.argv[1:],"hC:c:d:o:",["help"])
    except getopt.GetoptError:
        sys.exit()
    
    argsdict={}
    for opt,val in options:
        argsdict[opt]=val

    if '-h' in argsdict:
        print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')
    elif '--help' in argsdict:
        print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')   
    if '-C' in argsdict:
        rconfig = Config(argsdict['-c'],argsdict['-C'])
    else:
        rconfig = Config(argsdict['-c'],'DEFAULT')
    configdict = rconfig.readConfig()
     

    userdata = UserData(argsdict['-d'])
    userdata.run()

    calresult = CalcuResult(configdict)
    calresult.run() 

    wresult = WriteResult(argsdict['-o'])
    wresult.run()


