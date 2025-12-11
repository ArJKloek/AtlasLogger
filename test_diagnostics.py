#!/usr/bin/env python3
"""Test script to read SMTC board diagnostic values (temperature and 5V supply)."""

import time
import sys

try:
    import sm_tc
except ImportError:
    print("ERROR: sm_tc library not found!")
    print("Install it with: cd smtc/python && sudo pip3 install .")
    sys.exit(1)


def main():
    """Read and display diagnostic temperature and 5V supply voltage."""
    print("=" * 60)
    print("SMTC Board Diagnostics Test")
    print("=" * 60)
    
    try:
        # Initialize SMTC card at stack level 0
        print("\nInitializing SMTC card (stack 0)...")
        device = sm_tc.SMtc(0)
        print("✓ Card initialized successfully")
        
        print("\n" + "-" * 60)
        print("Reading diagnostic values (Ctrl+C to stop)...")
        print("-" * 60)
        print(f"{'Time':<12} {'Board Temp (°C)':<18} {'5V Supply (V)':<15}")
        print("-" * 60)
        
        # Continuous reading loop
        while True:
            try:
                # Read diagnostic temperature
                diag_temp = device.get_diag_temperature()
                
                # Read 5V supply voltage
                supply_5v = device.get_diag_5v()
                
                # Get current time
                current_time = time.strftime("%H:%M:%S")
                
                # Display readings
                print(f"{current_time:<12} {diag_temp:>16.2f}  {supply_5v:>13.2f}")
                
                # Wait 1 second before next reading
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n\nStopped by user")
                break
            except Exception as e:
                print(f"\n[ERROR] Failed to read diagnostic values: {e}")
                time.sleep(1)
        
    except Exception as e:
        print(f"\n[ERROR] Failed to initialize SMTC card: {e}")
        print("\nTroubleshooting:")
        print("  - Check that the SMTC card is properly connected")
        print("  - Verify I2C is enabled (sudo raspi-config)")
        print("  - Check stack level is correct (default is 0)")
        print("  - Ensure sm_tc library is up to date")
        sys.exit(1)


if __name__ == "__main__":
    main()
