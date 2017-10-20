#!/usr/bin/env python3

import sys
import os

class Config(object):
    def __init__(self,configfile):
        self._configfile = configfile
        self._configdict = {}
    
        try:
            if os.path.exists('./{0}'.format(self._configfile)) == False:
                raise ValueError()
            elif self._configfile[-3:] != 'cfg':
                raise ValueError()
             
            
            with open('./{0}'.format(self._configfile)) as cfile:
                for tmpline in cfile:
                    tmpstr = tmpline.split('=')
                    self._configdict[tmpstr[0].strip()]=float(tmpstr[1].strip()) 
        except ValueError:
            print('Parameter Error')
            sys.exit(-1)
    def get_configdict(self):
        return self._configdict   
            
class UserData(object):

    def __init__(self,userfile):
        self._userfile = userfile
        self._userdict = {}

        try:
            if os.path.exists('./{0}'.format(self._userfile)) == False:
                raise ValueError()
            elif self._userfile[-3:] != 'csv':
                raise ValueError()


            with open('./{0}'.format(self._userfile)) as ufile:
                for tmpline in ufile:
                    tmpstr = tmpline.split(',')
                    self._userdict[int(tmpstr[0].strip())]=int(tmpstr[1].strip())
        except ValueError:
            print('Parameter Error')
            sys.exit(-1)
    def get_userdict(self):
        return self._userdict




def calShebao(salary,configdict):
      
    tmp=salary
    if salary < configdict['JiShuL']:
        tmp = configdict['JiShuL']
    elif salary > configdict['JiShuH']:
        tmp = configdict['JiShuH']

    sheBao = tmp*(configdict['YangLao'] + configdict['YiLiao'] + configdict['ShiYe'] + configdict['GongShang'] + configdict['ShengYu'] + configdict['GongJiJin'])
    return sheBao

   
def calTax(salary,sbMoney):
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



if __name__ == "__main__":

    args = sys.argv[1:]
   
    index = args.index('-c')
    configfile = args[index+1]
    rconfig = Config(configfile)
    configdict = rconfig.get_configdict()


    index = args.index('-d')
    userfile = args[index+1]
    userdata = UserData(userfile)
    userdict = userdata.get_userdict()



    outputList = []
    
    for tmpstr in userdict.items():
        sheBao = calShebao(tmpstr[1],configdict)
        tax = calTax(tmpstr[1],sheBao)
        shifa = tmpstr[1] - sheBao - tax
        
        tmpLine = '{0},{1},{2:.2f},{3:.2f},{4:.2f}\n'.format(tmpstr[0],tmpstr[1],sheBao,tax,shifa)
        outputList.append(tmpLine)
   
    outputList.sort()
    
    index = args.index('-o')
    outputfile = args[index+1]
    with open('./{0}'.format(outputfile),'w') as ofile:
        for tmpLine in outputList:
            ofile.write(tmpLine)

