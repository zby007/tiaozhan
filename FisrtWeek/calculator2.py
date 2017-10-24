#!/usr/bin/env python3

import sys

def calShebao(salary):
    sheBao = salary*(0.08 + 0.02 + 0.005 + 0.06)
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

    try:
        lenInput = len(sys.argv)
        if lenInput < 2:
            raise ValueError()
        else:
            salList = sys.argv[1:]       
            salDict={}
            for tmpStr in salList:
                keyStr = tmpStr.split(':')
                gongHao = int(keyStr[0])
                salary = int(keyStr[1])

                sheBao = calShebao(salary)
                tax = calTax(salary,sheBao)
                finalSal = salary - sheBao -tax
                salDict[gongHao] = finalSal
            
            for key,value in salDict.items():
                print("{0}:{1:.2f}".format(key,value))
            
           
    except ValueError:
        print("Parameter Error")

