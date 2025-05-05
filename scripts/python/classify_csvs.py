import csv
import os
from multiprocessing import Pool


def classify_rows(input):

    input_file = f"/ifs/groups/rosenMRIGrp/kr3288/extended/DM_pipeline/thresholds/{input}"
    output_file = f"/ifs/groups/rosenMRIGrp/kr3288/extended/DM_pipeline/final/{input}"
    rows = []
    
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            score = float(row[2])          # 3rd column (0-indexed)
            threshold = float(row[4])      # 5th column (0-indexed)
            
            # Determine classification
            classification = "Known" if score > threshold else "Unknown"
            
            # Add the classification to the row
            new_row = row + [classification]
            rows.append(new_row)
    
    # Write the results to the output CSV file
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    print(f"Processed {len(rows)} rows.")
    print(f"Results saved to {output_file}")

if __name__ == "__main__":

    input = os.listdir('/ifs/groups/rosenMRIGrp/kr3288/extended/DM_pipeline/thresholds')

    num_threads = int(os.environ.get('SLURM_NTASKS', 24))
    with Pool(processes=num_threads) as pool:
        pool.map(classify_rows, input)

