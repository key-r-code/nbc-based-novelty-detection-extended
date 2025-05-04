import polars as pl
import os
from multiprocessing import Pool

def merge_files(lengths_file):
    """
    Merge two CSV files based on sequence ID.
    No headers in output.
    
    Args:
        lengths_file (str): Path to the file with sequence IDs and lengths
        other_data_file (str): Path to the file with sequence IDs, positions, and scores
        output_file (str): Path to the output CSV file
    """

    length_file = f"/ifs/groups/rosenMRIGrp/kr3288/extended/DM_pipeline/lengths/{lengths_file}"
    original_file = f"/ifs/groups/rosenMRIGrp/kr3288/extended/DM_pipeline/all_csvs/{lengths_file[:-11]}.csv"
    output_file = f"/ifs/groups/rosenMRIGrp/kr3288/extended/DM_pipeline/merge/{lengths_file[:-11]}_merged.csv"

    lengths_df = pl.read_csv(
        length_file,
        has_header=False,
        new_columns=["Sequence_ID", "Length"]
    )
    
    other_df = pl.read_csv(
        original_file,
        has_header=False,
        new_columns=["Sequence_ID", "Position", "Score"]
    )
    
    merged_df = other_df.join(
        lengths_df,
        on="Sequence_ID",
        how="left"
    )
    
    with open(output_file, 'w') as f:
        for row in merged_df.rows():
            f.write(','.join(str(val) for val in row) + '\n')
    
    print(f"Merged {len(other_df)} rows from the other file with length data.")
    print(f"Results saved to {output_file} (without headers).")


if __name__ == "__main__":

    lengths_file = os.listdir('/ifs/groups/rosenMRIGrp/kr3288/extended/DM_pipeline/lengths')

    num_threads = int(os.environ.get('SLURM_NTASKS', 24))
    with Pool(processes=num_threads) as pool:
        pool.map(merge_files, lengths_file)