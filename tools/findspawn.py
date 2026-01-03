import struct
import sys

def read_player_start(wad_path):
    try:
        with open(wad_path, 'rb') as f:
            # 1. Read Header (12 bytes)
            header = f.read(12)
            identification, num_lumps, info_table_offset = struct.unpack('<4sII', header)

            if identification not in [b'IWAD', b'PWAD']:
                print("Not a valid WAD file.")
                return

            # 2. Read Directory
            f.seek(info_table_offset)
            lumps = []
            for _ in range(num_lumps):
                entry = f.read(16)
                offset, size, name = struct.unpack('<II8s', entry)
                lumps.append({
                    'offset': offset,
                    'size': size,
                    'name': name.decode('ascii').strip('\x00')
                })

            # 3. Look for E1M1 and the subsequent THINGS lump
            found_map = False
            for i, lump in enumerate(lumps):
                if lump['name'] == 'E1M1':
                    found_map = True

                if found_map and lump['name'] == 'THINGS':
                    f.seek(lump['offset'])
                    # Each THING entry is 10 bytes
                    num_things = lump['size'] // 10

                    print(f"--- Analyzing THINGS lump ({num_things} objects found) ---")
                    for _ in range(num_things):
                        data = f.read(10)
                        # Structure: x(short), y(short), angle(short), type(short), options(short)
                        x, y, angle, t_type, opts = struct.unpack('<hhhhh', data)

                        if t_type == 1: # Type 1 = Player 1 Start
                            print(f"PLAYER 1 FOUND:")
                            print(f"  WAD Coordinates: X={x}, Y={y}")
                            print(f"  Fixed Point Conversion (16.16): X={x << 16}, Y={y << 16}")
                            print(f"  Starting Angle: {angle}°")
                            return

            if not found_map:
                print("E1M1 not found in WAD.")
            else:
                print("THINGS lump not found for E1M1.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 read_player_start.py your_file.wad")
    else:
        read_player_start(sys.argv[1])
