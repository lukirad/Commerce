from django.test import TestCase

# Create your tests here.

n = int(input())
i = 0
outcome = str()
while i <= n:
    outcome = outcome + str(i)
    i += 1
print(outcome)