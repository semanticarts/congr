import csv

input_file = "first-full-dir-scan.ttl"
output_file = "output.csv"

directories = []

with open(input_file, "r") as file:
    lines = file.readlines()

for line in lines:
    if line.startswith("congr:pathString"):
        path = line.split('"')[1]
        directories.append(path)

with open(output_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Directory"])

    for directory in directories:
        writer.writerow([directory])
