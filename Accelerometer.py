import smbus2
import time

# Code adapted from Bing Copilot
# Accelerometer model MMA7660FC

I2C_BUS = 1
ACCEL_ADDRESS = 0x4C # to be changed

# Registers, confirmed thru datasheets

ACCEL_REG_XO = 0x00
ACCEL_REG_YO = 0x01
ACCEL_REG_ZO = 0x02
ACCEL_REG_MO = 0x07

# Init Bus

bus = smbus2.SMBus(I2C_BUS)

def read_acceleration():
    # Read X, Y, Z accel values

    x = bus.read_byte_data(ACCEL_ADDRESS, ACCEL_REG_XO)
    y = bus.read_byte_data(ACCEL_ADDRESS, ACCEL_REG_YO)
    z = bus.read_byte_data(ACCEL_ADDRESS, ACCEL_REG_ZO)

    # Convert values to signed 6-bit ints
    x = x if x < 32 else x - 64
    y = y if y < 32 else y - 64
    z = z if z < 32 else z - 64

    return x, y, z

def main():
    bus.write_byte_data(ACCEL_ADDRESS,ACCEL_REG_MO,0x01)
    try:
        while True:
            x, y, z = read_acceleration()
            print(f"({x},{y},{z})")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Program terminated")
    finally:
        # Set Accelerometer to standby mode
        bus.write_byte_data(ACCEL_ADDRESS,ACCEL_REG_MO,0x00)
        bus.close()

if __name__ == "__main__":
    main()

