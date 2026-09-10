import numpy as np
arr = np.array([45,27,33,15,21,96])
print(arr)
print(type(arr))

print(arr[0])
print(arr[-1])

print("Slicing:",arr[2:5])

print(arr.dtype)

arr = np.array([45,27,33,15,21,96],dtype="S")
print(arr)
print(arr.dtype)

arr1 = np.array([[1,2,3,4],[5,6,7,8]])

print(arr1.shape)

arr2 = np.array([1,2,3,4,5,6,7,8,9,10,11,12])
newarr = arr2.reshape(4,3)
print(newarr)

for i in arr:
    print(i)

arr3 = np.array([12,34,56,78,90])
join_arr = np.concatenate((arr,arr3))
print(join_arr)