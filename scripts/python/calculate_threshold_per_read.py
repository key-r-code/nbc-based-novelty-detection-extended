import csv
import os
from multiprocessing import Pool

def process_csv(input):
    """
    Process a CSV file and add the result of a formula as a 5th column.

    Args:
        input_file (str): Path to the input CSV file
        output_file (str): Path to the output CSV file
    """
    rows = []

    input_file = f"/ifs/groups/rosenMRIGrp/kr3288/extended/DM_pipeline/merge1/{input}"
    output_file = f"/ifs/groups/rosenMRIGrp/kr3288/extended/DM_pipeline/thresholds/{input[:-11]}.csv"

    # Read the input CSV file
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # Get the length value from the 4th column (0-indexed)
            length = float(row[3])

            # Calculate the threshold using the new formula
            threshold = -10.478 * length

            # Add the threshold value to the row
            new_row = row + [str(threshold)]
            rows.append(new_row)

    # Write the results to the output CSV file
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"Processed {len(rows)} rows.")
    print(f"Results saved to {output_file}")

if __name__ == "__main__":

    input = os.listdir('/ifs/groups/rosenMRIGrp/kr3288/extended/DM_pipeline/merge1')

    num_threads = int(os.environ.get('SLURM_NTASKS', 24))
    with Pool(processes=num_threads) as pool:
        pool.map(process_csv, input)