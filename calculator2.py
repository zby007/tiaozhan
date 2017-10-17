#!/usr/bin/env python3

import sys


if __name__ == "__main__":

    try:
        
        if len(sys.argv) < 2:
            raise ValueError()
        else:
            salDict=sys.argv[1].split(':')
            print(salDict)
 
    except ValueError:
        print("Parameter Error")


   
'''
try:
    if len(sys.argv) > 2:
        raise ValueError()
    
    salary=int(sys.argv[1])   

    taxMoney = salary - 0 -3500
  
    if salary <= 3500:          
        print(format(0,".2f"))
    elif taxMoney <=1500:
        finalTax = taxMoney * 0.03 - 0    
        print(format(finalTax,".2f"))
    elif taxMoney <=4500: 
        finalTax = taxMoney * 0.1 - 105        
        print(format(finalTax,".2f"))

    elif taxMoney <=9000: 
        finalTax = taxMoney * 0.2 - 555        
        print(format(finalTax,".2f"))

    elif taxMoney <=35000: 
        finalTax = taxMoney * 0.25 - 1005        
        print(format(finalTax,".2f"))

    elif taxMoney <=55000: 
        finalTax = taxMoney * 0.3 - 2755        
        print(format(finalTax,".2f"))

    elif taxMoney <=80000: 
        finalTax = taxMoney * 0.35 - 5505        
        print(format(finalTax,".2f"))

    else: 
        finalTax = taxMoney * 0.45 - 13505        
        print(format(finalTax,".2f"))

except ValueError:
    print("Parameter Error")
'''
