import codecs, statistics 
with codecs.open("out.txt", "r", 'utf-8') as f:
    data=f.readlines()
    data=data[0:300000]

words=0
nums=[]
oof=0
for line in data:
    num = len(line)
    words+=num
    nums.append(num)


print("average:",words//len(data))
print("max:",max(nums))
print("minim:",min(nums))
print("standard deviation:", statistics.stdev(nums))