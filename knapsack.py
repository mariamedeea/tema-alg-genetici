f = open("file.txt")
k = f.readline()
k = int(k)

s = [int(i) for i in f.readline().split()]

n = len(s)
sol = [0] * (k+1)
print(s)

print(sol)
for i in range(0, n):
    for j in range(k, -1, -1):
        if s[i] <= j:
            sol[j] = max(sol[j], sol[j-s[i]] + s[i])
            

print(sol[k])