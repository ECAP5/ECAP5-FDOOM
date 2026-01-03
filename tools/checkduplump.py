import struct
import sys
import os
from collections import defaultdict

def analyze_wad_duplicates(filename):
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return

    with open(filename, "rb") as f:
        # Read WAD header
        header_data = f.read(12)
        magic, num_lumps, dir_offset = struct.unpack("<4sII", header_data)

        f.seek(dir_offset)

        # Dictionary to store indices for each lump name
        lump_map = defaultdict(list)

        # Read the entire directory
        for i in range(num_lumps):
            entry_data = f.read(16)
            if len(entry_data) < 16: break

            file_pos, size, name_raw = struct.unpack("<II8s", entry_data)
            
            # Clean Doom name (8 chars max, stops at first \0)
            name = name_raw.split(b'\0')[0].decode('ascii', errors='ignore').upper()

            # Store index and info for the report
            lump_map[name].append({'index': i, 'pos': file_pos, 'size': size})

    print("-" * 60)
    print(f"DUPLICATE REPORT: {filename}")
    print("-" * 60)

    has_duplicates = False

    for name, occurrences in lump_map.items():
        if len(occurrences) > 1:
            has_duplicates = True
            print(f"[!] DUPLICATE DETECTED: '{name}' ({len(occurrences)} times)")
            for occ in occurrences:
                print(f"    -> Index: {occ['index']:<4} | Pos: 0x{occ['pos']:08X} | Size: {occ['size']}")

    if not has_duplicates:
        print("[V] No exact duplicates found in the directory.")

    print("-" * 60)

def main():
    if len(sys.argv) < 2:
        print("Usage: python find_wad_duplicates.py <file.wad>")
        sys.exit(1)
    analyze_wad_duplicates(sys.argv[1])

if __name__ == "__main__":
    main()
