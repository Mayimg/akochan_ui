#!/usr/bin/env python
import os
import sys
import subprocess
import argparse
from pathlib import Path

def process_year_directory(year, month=None):
    """
    Process all date directories within a specified year directory.
    
    Args:
        year: Year string (e.g., '2023' or '20xx')
        month: Optional month string (e.g., '01', '12'). If None, process all months.
    """
    # Set up environment for libai.so
    env = os.environ.copy()
    current_dir = Path.cwd()
    if 'LD_LIBRARY_PATH' in env:
        env['LD_LIBRARY_PATH'] = f"{current_dir}:{env['LD_LIBRARY_PATH']}"
    else:
        env['LD_LIBRARY_PATH'] = str(current_dir)
    
    # Base directory containing the logs
    base_dir = Path("tenhou_mjailog") / year
    
    if not base_dir.exists():
        print(f"Error: Directory {base_dir} does not exist!")
        return 1
    
    # Get all date directories (format: 20xxxxxx)
    if month:
        # Filter directories for specific month
        date_dirs = sorted([d for d in base_dir.iterdir() 
                           if d.is_dir() and d.name[4:6] == month])
    else:
        # Get all directories
        date_dirs = sorted([d for d in base_dir.iterdir() if d.is_dir()])
    
    if not date_dirs:
        if month:
            print(f"No date directories found for month {month} in {base_dir}")
        else:
            print(f"No date directories found in {base_dir}")
        return 1
    
    if month:
        print(f"Found {len(date_dirs)} date directories for month {month} in {base_dir}")
    else:
        print(f"Found {len(date_dirs)} date directories in {base_dir}")
    
    # Create output directory
    output_dir = Path("features")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each date directory
    successful = 0
    failed = 0
    
    for date_dir in date_dirs:
        # Build the command
        cmd = [
            sys.executable,
            "main.py",
            "--dump_feature",
            "--input_logdir", str(date_dir),
            "--input_regex", "*.json",
            "--output_npzdir", str(output_dir)
        ]
        
        print(f"\nProcessing {date_dir.name}...")
        print(f"Command: {' '.join(cmd)}")
        
        try:
            # Run the command with updated environment
            result = subprocess.run(cmd, capture_output=True, text=True, env=env)
            
            if result.returncode == 0:
                print(f"✓ Successfully processed {date_dir.name}")
                successful += 1
            else:
                print(f"✗ Failed to process {date_dir.name}")
                print(f"  Error: {result.stderr}")
                failed += 1
                
        except Exception as e:
            print(f"✗ Exception while processing {date_dir.name}: {e}")
            failed += 1
    
    # Summary
    print(f"\n{'='*50}")
    if month:
        print(f"Processing complete for year {year}, month {month}")
    else:
        print(f"Processing complete for year {year}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total: {len(date_dirs)}")
    print(f"{'='*50}")
    
    return 0 if failed == 0 else 1

def main():
    parser = argparse.ArgumentParser(
        description="Batch process tenhou_mjailog JSON files to extract features"
    )
    parser.add_argument(
        "year",
        help="Year to process (e.g., 2023 or 20xx)"
    )
    parser.add_argument(
        "--month",
        help="Month to process (e.g., 01, 02, ..., 12). If not specified, process all months",
        choices=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    )
    
    args = parser.parse_args()
    
    return process_year_directory(args.year, args.month)

if __name__ == "__main__":
    sys.exit(main())