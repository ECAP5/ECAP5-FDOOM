import struct
import sys
import os

def analyze_wad(filename):
    if not os.path.exists(filename):
        print(f"Erreur : Le fichier '{filename}' est introuvable.")
        return

    file_size = os.path.getsize(filename)

    with open(filename, "rb") as f:
        # 1. Lecture du Header (12 octets)
        # Format : < (Little Endian), 4s (char[4]), I (uint32), I (uint32)
        header_data = f.read(12)
        magic, num_lumps, dir_offset = struct.unpack("<4sII", header_data)
        
        try:
            magic_str = magic.decode('ascii')
        except:
            magic_str = "CORRUPTED"

        print("-" * 50)
        print(f"ANALYSE DU WAD : {filename}")
        print(f"Taille du fichier : {file_size} octets")
        print("-" * 50)
        print(f"Identification     : {magic_str}")
        print(f"Nombre de Lumps    : {num_lumps}")
        print(f"Offset Répertoire  : 0x{dir_offset:08X}")
        print("-" * 50)

        if dir_offset >= file_size:
            print("ERREUR : L'offset du répertoire est en dehors du fichier !")
            return

        # 2. Positionnement au début du répertoire
        f.seek(dir_offset)

        print(f"{'Index':<6} | {'Nom':<10} | {'FilePos':<12} | {'Taille':<10}")
        print("-" * 50)

        # 3. Parcours du dictionnaire
        for i in range(num_lumps):
            # Chaque entrée fait 16 octets
            entry_data = f.read(16)
            if len(entry_data) < 16:
                print(f"\n[!] Fin de fichier prématurée à l'index {i}")
                break

            file_pos, size, name_raw = struct.unpack("<II8s", entry_data)
            
            # Décodage du nom (nettoyage des caractères non-ASCII ou nuls)
            name = "".join([chr(b) for b in name_raw if 32 <= b <= 126])

            # On affiche tout ou une partie (ici les 30 premiers pour le debug)
            # Tu peux changer cette condition pour tout voir si besoin
            print(f"{i:<6} | {name:<10} | 0x{file_pos:08X} | {size:<10}")
            

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_wad.py <nom_du_fichier.wad>")
        sys.exit(1)

    analyze_wad(sys.argv[1])

if __name__ == "__main__":
    main()
