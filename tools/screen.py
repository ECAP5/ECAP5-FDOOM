import pygame
import numpy as np
import pyftdi.serialext
import time
import serial

# --- CONFIGURATION ---
FTDI_URL = 'ftdi://ftdi:232r/1'
BAUD_RATE = 115200

WIDTH, HEIGHT = 160, 100 # 16,000 pixels
EXPECTED_BYTES = WIDTH * HEIGHT

# Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH * 6, HEIGHT * 6))
pygame.display.set_caption("ECP5 Doom Debug via FTDI")

def rgb565_to_rgb888(raw_bytes):
    data16 = np.frombuffer(raw_bytes, dtype=np.uint16)
    r = ((data16 >> 11) & 0x1F) << 3
    g = ((data16 >> 5) & 0x3F) << 2
    b = (data16 & 0x1F) << 3
    rgb = np.stack((r, g, b), axis=-1).astype(np.uint8)
    return rgb.reshape((HEIGHT, WIDTH, 3))

def rgb222_to_rgb888(raw_bytes):
    data8 = np.frombuffer(raw_bytes, dtype=np.uint8)
    r = ((data8 >> 6) & 0x3) * 85
    g = ((data8 >> 4) & 0x3) * 85
    b = ((data8 >> 2) & 0x3) * 85
    rgb = np.stack((r, g, b), axis=-1).astype(np.uint8)
    return rgb.reshape((HEIGHT, WIDTH, 3))

def rgb323_to_rgb888(raw_bytes):
    data8 = np.frombuffer(raw_bytes, dtype=np.uint8)
    r = ((data8 >> 5) & 0x7) * 32
    g = ((data8 >> 3) & 0x3) * 64
    b = ((data8)      & 0x7) * 32
    rgb = np.stack((r, g, b), axis=-1).astype(np.uint8)
    return rgb.reshape((HEIGHT, WIDTH, 3))

def greyscale_to_rgb888(raw_bytes):
    data8 = np.frombuffer(raw_bytes, dtype=np.uint8)
    r = (data8)
    g = (data8)
    b = (data8)
    rgb = np.stack((r, g, b), axis=-1).astype(np.uint8)
    return rgb.reshape((HEIGHT, WIDTH, 3))

def rgb8888(raw_bytes):
    data32 = np.frombuffer(raw_bytes, dtype=np.uint32)
    # Note: Fixed potential typo from original (data8 -> data32)
    r = ((data32 >> 24) & 0xFF)
    g = ((data32 >> 16) & 0xFF)
    b = ((data32 >> 8) & 0xFF)
    rgb = np.stack((r, g, b), axis=-1).astype(np.uint8)
    return rgb.reshape((HEIGHT, WIDTH, 3))

def main():
    try:
        port = pyftdi.serialext.serial_for_url(FTDI_URL, baudrate=BAUD_RATE, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        print(f"Connected to {FTDI_URL}")

        buffer = b""
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Read in small blocks to avoid overflow
            data = port.read(2 * EXPECTED_BYTES)
            if data:
                buffer = data

            # Search for "NEXT" keyword in the buffer (frame delimiter)
            if b"NEXT" in buffer:
                parts = buffer.split(b"NEXT")
                if(len(parts) > 2):
                    part = parts[1]

                    # Ensure we have enough bytes after the "NEXT" tag
                    raw_frame = part + bytes([0 for x in range(EXPECTED_BYTES - len(part))])

                    print(f"First byte of frame: {raw_frame[0]}")

                    # Graphic Update
                    img_array = greyscale_to_rgb888(raw_frame)
                    surface = pygame.surfarray.make_surface(img_array.swapaxes(0, 1))
                    screen.blit(pygame.transform.scale(surface, screen.get_size()), (0, 0))
                    pygame.display.flip()

                # Clear processed buffer
                buffer = b""

    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
