import numpy as np 

x=np.zeros(4)
y=np.zeros(4)

for i in range(4):
    x[i]=i*i+3
    y[i]= i*i+7

x_v1=   np.flipud(np.transpose(np.array(np.vstack([x, y]))))
x_v2=   np.transpose(np.array(np.vstack([x, y])))
print(x_v1)
print("---------------------------")
print(x_v2)
print("---------------------------")
x_v=np.hstack((x_v1,x_v2))

print(x_v)
