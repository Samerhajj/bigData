#!/usr/bin/python3

import sys

def mapper():
    # Provide the path to your data file
  
        for line in sys.stdin:
            columns = line.strip().split(',')
            year = int(columns[0])  # Remove BOM if present
            for month in range(1, 13):
                value = float(columns[month])
                # Emit the intermediate key-value pair
                print(f"{year}\t{month}\t{value}")


if __name__ == "__main__":
    mapper()
