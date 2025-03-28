import os
import glob

def make(params):
    """Create a sequential pipeline for each input file in the directory"""
    
    pattern = os.path.join(params['input_directory'], params['file_pattern'])
    input_files = glob.glob(pattern)
        
    tasks = []
    
    for i, input_file in enumerate(input_files):
        file_name = os.path.basename(input_file).replace('.gz', '')
        
        file_tasks = [
            {
                'source': 'tasks/gunzip.py',
                'name': f'gunzip_{i}',
                'product': f'products/{file_name}',
                'params': {
                    'input_file': input_file,
                    'input_file_name': file_name
                }
            },
            {
                'source': 'tasks/create_fna.py',
                'name': f'create_fna_{i}',
                'product': f'products/{file_name}.fna',
                'upstream': [f'gunzip_{i}'],
                'params': {
                    'input_file_name': file_name
                }
            },
            {
                'source': 'tasks/create_directory.py',
                'name': f'create_directory_{i}',
                'product': f'products/{file_name}_dir',
                'upstream': [f'create_fna_{i}'],
                'params': {
                    'output_dir': f'{file_name}_dir'
                }
            },
            {
                'source': 'tasks/split_fna.py',
                'name': f'split_fna_{i}',
                'product': [f'products/{file_name}_dir/chunk_{j+1}.fna' for j in range(params['num_chunks'])],
                'upstream': [f'create_directory_{i}'],
                'params': {
                    'output_dir': f'{file_name}_dir',
                    'num_chunks': params['num_chunks']
                }
            },
            {
                'source': 'tasks/create_bash.py',
                'name': f'create_bash_{i}',
                'product': [f'products/{file_name}_dir/run_all.sh'],
                'upstream': [f'split_fna_{i}'],
                'params': {
                    'output_dir': f'{file_name}_dir'
                }
            }
        ]
        
        tasks.extend(file_tasks)
    
    return tasks