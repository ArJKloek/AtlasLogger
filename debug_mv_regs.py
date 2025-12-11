#!/usr/bin/env python3
"""
Debug: read raw mV registers to confirm address/scale.
Reads channels 1-8 from base address 54 (TCP_MV1_ADD) and prints raw + scaled mV.
"""
import sys
import struct

try:
    import smbus2
except ImportError:
    print("ERROR: smbus2 not installed. pip3 install smbus2")
    sys.exit(1)

BASE = 54  # current _TCP_MV1_ADD
ADDR = 0x16  # stack 0 base address; adjust if stacked (0x16 + stack)
BUS_NO = 1


def main():
    bus = smbus2.SMBus(BUS_NO)
    print(f"Reading raw mV registers from I2C addr 0x{ADDR:02x}, base={BASE}")
    print(f"{'CH':>3} | {'Addr':>4} | {'Raw':>6} | {'mV':>8}")
    print('-' * 30)
    for ch in range(1, 9):
        addr = BASE + (ch - 1) * 2
        try:
            buff = bus.read_i2c_block_data(ADDR, addr, 2)
            raw = struct.unpack('h', bytearray(buff))[0]
            mv = raw / 100.0
            print(f"{ch:3d} | {addr:4d} | {raw:6d} | {mv:8.3f}")
        except Exception as e:
            print(f"{ch:3d} | {addr:4d} | ERROR: {e}")
    bus.close()


if __name__ == "__main__":
    main()
