import csv
import random

# Open the original CSV file to read and a new CSV file to write
with open('../creditcard_backup.csv', mode='r') as infile, open('../creditcard.csv', mode='w', newline='') as outfile:
    # Create a csv reader object to read from the original file
    reader = csv.reader(infile)
    # Create a csv writer object to write to the new file
    writer = csv.writer(outfile)

    # Read the header (first row) from the original file
    header = next(reader)
    # Insert the 'user_id' column at the second position
    header.insert(1, 'user_id')
    # Write the modified header to the new file
    writer.writerow(header)

    # Iterate through each row in the original file
    for row in reader:
        # Generate a random number between 1 and 1000 for the user_id
        user_id = random.randint(1, 1000)
        # Insert the generated user_id at the second position of the current row
        row.insert(1, user_id)
        # Write the modified row to the new file
        writer.writerow(row)

print("New CSV file with user_id column added has been created.")
