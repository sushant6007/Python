arr = [1,4,6,4,9,3,5,9,-1,-5,55,45]
k = 3
min_sum = 10000

for i in range(0, len(arr)-k):
    # sum = arr[i]+arr[i+1]+arr[i+2]
    sum2 = sum(arr[i:i+3])
    if sum2 < min_sum:
        min_sum = sum2
        
print(min_sum)
