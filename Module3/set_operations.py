#union
from calendar import different_locale

set_1 = {1,2,3}
set_2 = {3,4,5}

union_result_method = set_1.union(set_2)
union_result_operator = set_1 | set_2

print(union_result_method)
print(union_result_operator)


#intersection
intersection_result_method = set_1.intersection(set_2)
intersection_result_operator = set_1 & set_2

print(intersection_result_operator)
print(intersection_result_method)


#difference
difference_result_method = set_1.difference(set_2)
difference_operator = set_1.difference(set_2)

print(difference_operator)
print(difference_result_method)


#symentric difference
sd_method = set_1.difference(set_2)
sd_operator = set_1.difference(set_2)

print(sd_method)
print(sd_operator)