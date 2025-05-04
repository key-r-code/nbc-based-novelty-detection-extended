import os
import csv
from multiprocessing import Pool

def process_fasta_file(input):

    input_path = f"/ifs/groups/rosenMRIGrp/kr3288/extended/DM_pipeline/output/{input}/{input}.fasta"
    output_path = f"/ifs/groups/rosenMRIGrp/kr3288/extended/DM_pipeline/lengths/{input}_LENGTH.csv"
    current_id = ""
    current_seq = ""
    data = []
    
    with open(input_path, 'r') as fasta_file:
        for line in fasta_file:
            line = line.strip()
            
            if line.startswith('>'):
                if current_id and current_seq:
                    data.append((current_id, len(current_seq)))
                
                current_id = line[1:]  
                current_seq = ""
            else:                   
                current_seq += line
        
        if current_id and current_seq:
            data.append((current_id, len(current_seq)))
    
    with open(output_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Sequence_ID', 'Length'])  
        writer.writerows(data)
    
    print(f"Processed {len(data)} sequences.")
    print(f"Results saved to {output_path}")


if __name__ == "__main__":

    input_filenames = os.listdir('/ifs/groups/rosenMRIGrp/kr3288/extended/DM_pipeline/all_csvs')
    input_filenames = [filename[:-4] for filename in input_filenames]

    num_threads = int(os.environ.get('SLURM_NTASKS', 24))
    with Pool(processes=num_threads) as pool:
        pool.map(process_fasta_file, input_filenames)

