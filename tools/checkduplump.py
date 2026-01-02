import struct
import sys
import os
from collections import defaultdict

def analyze_wad_duplicates(filename):
    if not os.path.exists(filename):
        print(f"Erreur : Le fichier '{filename}' est introuvable.")
        return

    with open(filename, "rb") as f:
        header_data = f.read(12)
        magic, num_lumps, dir_offset = struct.unpack("<4sII", header_data)
        
        f.seek(dir_offset)

        # Dictionnaire pour stocker les index de chaque nom de lump
        lump_map = defaultdict(list)
        
        # Lecture de tout le répertoire
        for i in range(num_lumps):
            entry_data = f.read(16)
            if len(entry_data) < 16: break
            
            file_pos, size, name_raw = struct.unpack("<II8s", entry_data)
            # Nettoyage du nom Doom (8 caractères max, s'arrête au premier \0)
            name = name_raw.split(b'\0')[0].decode('ascii', errors='ignore').upper()
            
            # On stocke l'index et les infos pour le rapport
            lump_map[name].append({'index': i, 'pos': file_pos, 'size': size})

    print("-" * 60)
    print(f"RAPPORT DES DOUBLONS : {filename}")
    print("-" * 60)

    has_duplicates = False
    
    for name, occurrences in lump_map.items():
        if len(occurrences) > 1:
            has_duplicates = True
            print(f"[!] DOUBLON DÉTECTÉ : '{name}' ({len(occurrences)} fois)")
            for occ in occurrences:
                print(f"    -> Index: {occ['index']:<4} | Pos: 0x{occ['pos']:08X} | Taille: {occ['size']}")

    if not has_duplicates:
        print("[V] Aucun doublon exact trouvé dans le répertoire.")
    
    print("-" * 60)

def main():
    if len(sys.argv) < 2:
        print("Usage: python find_wad_duplicates.py <fichier.wad>")
        sys.exit(1)
    analyze_wad_duplicates(sys.argv[1])

if __name__ == "__main__":
    main()
