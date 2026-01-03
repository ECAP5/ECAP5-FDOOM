import struct
import sys
import os

def analyze_wad(filename):
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return

    file_size = os.path.getsize(filename)

    with open(filename, "rb") as f:
        # 1. Reading the Header (12 bytes)
        # Format: < (Little Endian), 4s (char[4]), I (uint32), I (uint32)
        header_data = f.read(12)
        magic, num_lumps, dir_offset = struct.unpack("<4sII", header_data)

        try:
            magic_str = magic.decode('ascii')
        except:
            magic_str = "CORRUPTED"

        print("-" * 50)
        print(f"WAD ANALYSIS: {filename}")
        print(f"File Size: {file_size} bytes")
        print("-" * 50)
        print(f"Identification     : {magic_str}")
        print(f"Number of Lumps    : {num_lumps}")
        print(f"Directory Offset   : 0x{dir_offset:08X}")
        print("-" * 50)

        if dir_offset >= file_size:
            print("ERROR: Directory offset is outside of the file boundary!")
            return

        # 2. Moving to the start of the directory
        f.seek(dir_offset)

        print(f"{'Index':<6} | {'Name':<10} | {'FilePos':<12} | {'Size':<10}")
        print("-" * 50)

        # 3. Iterating through the directory entries
        for i in range(num_lumps):
            # Each entry is 16 bytes
            entry_data = f.read(16)
            if len(entry_data) < 16:
                print(f"\n[!] Premature End of File (EOF) at index {i}")
                break

            file_pos, size, name_raw = struct.unpack("<II8s", entry_data)

            # Name decoding (cleaning non-ASCII or null characters)
            name = "".join([chr(b) for b in name_raw if 32 <= b <= 126])

            # Displaying entry data
            print(f"{i:<6} | {name:<10} | 0x{file_pos:08X} | {size:<10}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_wad.py <filename.wad>")
        sys.exit(1)

    analyze_wad(sys.argv[1])

if __name__ == "__main__":
    main()
