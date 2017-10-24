#!/usr/bin/env python3
import queue
import sys
from multiprocessing import Process,Queue



q_user = Queue()
q_result = Queue()



class Config(object):
    def __init__(self,configfile):
        self._configfile = configfile
        self._configdict = {}
        with open('{0}'.format(self._configfile)) as cfile:
            for tmpline in cfile:
                tmpstr = tmpline.split('=')
                self._configdict[tmpstr[0].strip()]=float(tmpstr[1].strip()) 

    def get_configdict(self):
        return self._configdict   
            
class UserData(Process):
    def run(self):
        index = args.index('-d')
        userfile = args[index+1]
        userdict = {}
        with open('{0}'.format(userfile)) as ufile:
            for tmpline in ufile:
                tmpstr = tmpline.split(',')
                userdict[int(tmpstr[0].strip())]=int(tmpstr[1].strip())
            q_user.put(userdict)



class CalcuResult(Process):

    def __init__(self,configdict):
        self._configdict = configdict

    def calShebao(self,salary):
        
        tmp=salary
        if salary < self._configdict['JiShuL']:
            tmp = self._configdict['JiShuL']
        elif salary > self._configdict['JiShuH']:
            tmp = self._configdict['JiShuH']

        sheBao = tmp*(self._configdict['YangLao'] + self._configdict['YiLiao'] + self._configdict['ShiYe'] + self._configdict['GongShang'] + self._configdict['ShengYu'] + self._configdict['GongJiJin'])
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

    def run(self):
        while True:
            try:         
                result = q_result.get(timeout=1)
            except queue.Empty:
                return
            result.sort()   
            index = args.index('-o')
            outputfile = args[index+1]
            with open('{0}'.format(outputfile),'w') as ofile:
                for tmpLine in result:
                    ofile.write(tmpLine)


if __name__ == "__main__":

    args = sys.argv[1:]
   
    index = args.index('-c')
    configfile = args[index+1]
    rconfig = Config(configfile)
    configdict = rconfig.get_configdict()


    userdata = UserData()
    userdata.run()

    calresult = CalcuResult(configdict)
    calresult.run() 

    wresult = WriteResult()
    wresult.run()



