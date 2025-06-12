
import csv
import sys

sys.setrecursionlimit(20000000)

from Les_2 import LinkedListEmpty


# Kies standaardbestand als er geen argument is
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "kentekens1000.txt"

kentekens = LinkedListEmpty()

with open(filename) as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        kentekens = kentekens.addFirst(row[0])

# Voor testdoeleinden:
aantal = kentekens.uniq()
print(aantal)

