def find_pythagorean_triplets():
  #TODO: Write - Your - Code
  arr = [1, 2, 3, 4, 5, 6, 8, 10, 16, 25]
  triplets = []
  a = [x*x for x in arr]
  print(a)
  for i in range(0, len(a)-2):
    for j in range(i+1, len(a)-1):
      lhs = a[i] + a[j]
      rhs = a[j+1:]
      print(a[i])
      print(a[j])
      print(rhs)

      l = 0
      r = len(rhs)-1
      m = (l+r)//2
      while l <= r:
        mid = rhs[m]
        if mid == lhs:
          triplets.append([a[i], a[j], mid])
          break
        elif mid < lhs:
            l = m + 1
        else:
            r = m - 1

  return triplets

print(find_pythagorean_triplets())

