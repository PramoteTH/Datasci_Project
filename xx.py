from subprocess import run
import subprocess
alls =[]

a = subprocess.check_output(["python3", "test.py", "-i", "./images/test.jpg"]).decode("utf-8")
l = a.split(' ')
for i in range(len(l)):
    print(l[i])
    alls.append(l[i])
    alls.append(" ")

 
def convert(alls):
    new = "" 
    for x in alls[2:-3]: 
        new += x  

    return new 

result = convert(alls)

