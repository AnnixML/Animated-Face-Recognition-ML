import csv

# Open the input CSV file
with open('../../tags_processed_stages/dafre_tags.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    data = list(reader)

# Create a dictionary to store unique values from column 5 and their corresponding column 6 values
column5_column6 = {}

# Iterate over rows starting from the second row
for row in data[1:]:
    column5_value = row[4]
    column6_value = row[5]

    if column6_value not in column5_column6:
        column5_column6[column6_value] = [column5_value]

# Open the output CSV file
with open('output.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)

    # Write the header row
    writer.writerow(['Column 5', 'Column 6'])

    # Write each unique pair of column 5 and column 6 to the output file
    for column5_value, column6_values in column5_column6.items():
        for column6_value in column6_values:
            writer.writerow([column5_value, column6_value])
            
with open('output.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    data = list(reader)

with open('output.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)

    writer.writerow(data[0])

    for row in data[1:]:
        column1_value = row[0]

        if len(column1_value.split(',')) > 1:
            continue

        writer.writerow([row[0][2:-2],row[1]])
        
with open('output.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    data = list(reader)

with open('output.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)

    writer.writerow(data[0])

    for row in data[1:]:
        column2_value = row[1][2:-2]

        column2_array = column2_value.split(',')

        row[1] = column2_array[-1].strip()
        if row[1][0] == "'":
            row[1] = row[1][1:]
        writer.writerow([row[0], row[1]])