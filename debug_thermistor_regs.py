#!/usr/bin/env python3
"""
Debug script to find correct thermistor register addresses.
Tests different potential base addresses for thermistor data.
"""

import sys
import struct

try:
    import smbus2
except ImportError:
    print("ERROR: smbus2 not found. Install with: pip3 install smbus2")
    sys.exit(1)

# Possible base addresses to test based on different calculations
POSSIBLE_BASES = [
    (24, "Current _I2C_THERMISTOR1_ADD (wrong calc)"),
    (101, "Recalculated minus LED registers"),
    (113, "Latest calculation with all registers"),
    (78, "Alternative calculation"),
]

def test_address(bus, base_addr, description):
    """Test reading thermistor data from a specific base address."""
    print(f"\n{description} (base={base_addr}):")
    print(f"  {'CH':>3} | {'Addr':>4} | {'Raw':>6} | {'Temp':>7}")
    print("  " + "-" * 35)
    
    for ch in range(1, 11):
        addr = base_addr + (ch - 1) * 2
        try:
            buff = bus.read_i2c_block_data(0x16, addr, 2)
            val = struct.unpack('h', bytearray(buff))[0]
            temp = val / 10.0
            marker = " ✓" if 15 < temp < 35 else ""  # Reasonable room temp
            print(f"  {ch:3d} | {addr:4d} | {val:6d} | {temp:7.1f}°C{marker}")
        except Exception as e:
            print(f"  {ch:3d} | {addr:4d} | ERROR: {str(e)[:20]}")

def main():
    """Test different thermistor base addresses."""
    try:
        bus = smbus2.SMBus(1)
        print("=" * 60)
        print("Thermistor Register Address Debug")
        print("=" * 60)
        print("Looking for ~20°C readings (200 raw value)")
        
        for base_addr, description in POSSIBLE_BASES:
            test_address(bus, base_addr, description)
        
        bus.close()
        print("\n" + "=" * 60)
        print("✓ marks readings in reasonable range (15-35°C)")
        
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        print("Make sure you're running with sudo and I2C is enabled")
        sys.exit(1)

if __name__ == "__main__":
    main()
