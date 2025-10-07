import numpy as np
from numpy.ma.extras import average

#creating a 20 array
arr_2d = np.array([[1,2,3,4,5], [6,7,8,9,10]])
print(arr_2d)

element = arr_2d[1,2]
print(element)

dimensions = arr_2d.ndim
print(dimensions)

arr_shape = arr_2d.shape
print(arr_shape)

sub_array = arr_2d[:2, :2]
print(sub_array)

sub_array_2 = arr_2d[-4:, -4:]
print(sub_array_2)

sub_array_3 = arr_2d[:, ::2]
print(sub_array_3)

#Satistical Operations
total_sum = np.sum(arr_2d)
print(total_sum)

total_sum = np.mean(arr_2d)
print(average)

sum_columns = np.sum(arr_2d, axis=0)
print(sum_columns)

sum_rows = np.sum(arr_2d, axis = 1)
print(sum_rows)
reshaped_array = arr_2d.reshape((5,2))
print(reshaped_array)