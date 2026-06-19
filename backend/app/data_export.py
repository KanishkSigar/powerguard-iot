import io
import csv
from typing import List, Dict

def generate_csv_export(data: List[Dict]) -> io.StringIO:
    """
    Generate a CSV file buffer from a list of historical readings.
    """
    buffer = io.StringIO()
    if not data:
        buffer.write("No data available\n")
        buffer.seek(0)
        return buffer

    # Extract all unique keys to form the header
    fieldnames = list(data[0].keys())
    
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow(row)
        
    buffer.seek(0)
    return buffer
