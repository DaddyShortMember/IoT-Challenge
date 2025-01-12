import smbus
import time

# Initialisation de l'I2C
bus = smbus.SMBus(1)  # Utilise I2C-1
address = 0x57        # Adresse du capteur Max30100

# Réinitialisation du capteur
def reset_sensor():
    bus.write_byte_data(address, 0x09, 0x00)  # Désactiver les LEDs
    bus.write_byte_data(address, 0x06, 0x00)  # Désactiver le mode
    time.sleep(0.1)
    bus.write_byte_data(address, 0x06, 0x03)  # Mode SpO2
    bus.write_byte_data(address, 0x09, 0x1F)  # Activer les LEDs
    print("Capteur réinitialisé.")

# Configurer le capteur en mode SpO2
def initialize_sensor():
    bus.write_byte_data(address, 0x06, 0x03)  # Mode SpO2
    time.sleep(0.5)
    bus.write_byte_data(address, 0x09, 0x1F)  # Activer les LEDs
    time.sleep(0.5)
    bus.write_byte_data(address, 0x08, 0x00) # config FIFO
    time.sleep(0.5)
    validate_config
    print("sensors configured")

# Lire les données brutes
def read_raw_data():
    data = bus.read_i2c_block_data(address, 0x00, 4)  # Lire 4 octets
    print(f"Raw data : {data}")
    return data

# Vérifier l'état des registres d'interruption et du FIFO
def check_interrupt_and_fifo():
    interrupt_status = bus.read_byte_data(address, 0x00)
    fifo_status = bus.read_byte_data(address, 0x02)
    print(f"Interruption state : {interrupt_status}")
    print(f"FIFO status : {fifo_status}")
    return interrupt_status, fifo_status

# Lire les données IR et Rouge
def read_sensor():
    data = read_raw_data()
    ir_data = (data[0] << 8) | data[1]  # Données IR
    red_data = (data[2] << 8) | data[3]  # Données Rouge
    return ir_data, red_data

def read_status_register():
    # Lire l'état des registres du capteur
    status = bus.read_byte_data(address, 0x00)
    print(f"Registre de statut : {status}")

def read_all_registers():
    # Lire et afficher les registres clés du capteur
    try:
        mode = bus.read_byte_data(address, 0x06)  # Mode de fonctionnement
        led_config = bus.read_byte_data(address, 0x09)  # Configuration LED
        fifo_config = bus.read_byte_data(address, 0x08)  # Configuration FIFO
        fifo_wr_ptr = bus.read_byte_data(address, 0x04)  # Pointeur FIFO Write
        fifo_rd_ptr = bus.read_byte_data(address, 0x06)  # Pointeur FIFO Read
        overflow = bus.read_byte_data(address, 0x07)    # FIFO Overflow Counter

        print(f"Mode : {mode}")
        print(f"LED Config : {led_config}")
        print(f"FIFO Config : {fifo_config}")
        print(f"FIFO Write Pointer : {fifo_wr_ptr}")
        print(f"FIFO Read Pointer : {fifo_rd_ptr}")
        print(f"FIFO Overflow Counter : {overflow}")

    except Exception as e:
        print(f"Erreur lors de la lecture des registres : {e}")

def validate_config():
    mode = bus.read_byte_data(address, 0x06)
    led_config = bus.read_byte_data(address, 0x09)
    fifo_config = bus.read_byte_data(address, 0x08)

    print(f"Mode actuel : {mode}")
    print(f"LED Config actuel : {led_config}")
    print(f"FIFO Config actuel : {fifo_config}")

    if mode != 3 or led_config != 31 or fifo_config != 0:
        print("Configuration incorrecte, vérifiez votre code ou capteur.")

def log_fifo_pointers():
    write_pointer = bus.read_byte_data(address, 0x04)
    read_pointer = bus.read_byte_data(address, 0x05)
    overflow_counter = bus.read_byte_data(address, 0x06)
    print(f"FIFO Write Pointer : {write_pointer}, Read Pointer : {read_pointer}, Overflow Counter : {overflow_counter}")

# Programme principal
try:
    read_all_registers()
    initialize_sensor()
    validate_config()
    while True:
        # Vérifier l'état du capteur et du FIFO
        check_interrupt_and_fifo()
        log_fifo_pointers()
        # Lire les données du capteur
        ir, red = read_sensor()
        print(f"IR: {ir}, Red: {red}")
        log_fifo_pointers()

        # Si les valeurs sont invalides (trop faibles), réinitialiser
        if ir == 0 and red < 100:
            print("Données faibles, réinitialisation du capteur.")
            reset_sensor()

        time.sleep(1)  # Attente avant la prochaine lecture

except KeyboardInterrupt:
    print("\nProgram ended.")

