import smbus2
import time
import socket
import logging
import subprocess
from datetime import datetime, timedelta

logging.basicConfig(filename='/var/log/oled_ip_display.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


CONFIG = {
    'OLED_ADDRESS': 0x3C,
    'I2C_BUS': 1,
    'IP_CHECK_TIMEOUT': 120,
    'IP_CHECK_INTERVAL': 5,
    'DISPLAY_UPDATE_INTERVAL': 30,
    'SERVICE_CHECK_INTERVAL': 20, 
    'SERVICE_NAME': 'main-server.service'  
}

bus = smbus2.SMBus(CONFIG['I2C_BUS'])



def oled_command(cmd):
    bus.write_byte_data(CONFIG['OLED_ADDRESS'], 0x00, cmd)

def oled_data(data):
    bus.write_byte_data(CONFIG['OLED_ADDRESS'], 0x40, data)

def init_oled():
    oled_command(0xAE)  
    oled_command(0xD5)  
    oled_command(0x80)
    oled_command(0xA8)  
    oled_command(0x1F)  
    oled_command(0xD3)  
    oled_command(0x00)
    oled_command(0x40)  
    oled_command(0x8D)  
    oled_command(0x14)
    oled_command(0x20)  
    oled_command(0x00)
    oled_command(0xA1)  
    oled_command(0xC8)  
    oled_command(0xDA)  
    oled_command(0x02)  
    oled_command(0x81)  
    oled_command(0xCF)
    oled_command(0xD9)  
    oled_command(0xF1)
    oled_command(0xDB)  
    oled_command(0x30)
    oled_command(0xA4)  
    oled_command(0xA6)  
    oled_command(0xAF)  

def clear_display():
    for page in range(4):  # 4 pages for 128*32
        oled_command(0xB0 + page)  
        oled_command(0x00)         
        oled_command(0x10)        
        for i in range(128):
            oled_data(0x00)

def display_text(text, row):
    oled_command(0xB0 + row)  
    oled_command(0x00)        
    oled_command(0x10)        
    for char in text:
        if char in font:
            for col in font[char]:
                oled_data(col)
        else:
            for _ in range(5):
                oled_data(0x00)
        oled_data(0x00)  

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2) 
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            return ip
        except (socket.timeout, socket.error):
            return None
        finally:
            s.close()
    except Exception as e:
        logging.error(f"Socket creation error: {e}")
        return None

def check_service_status(service_name):
    """
    (is_active, status_message)
    """
    try:
        result = subprocess.run(['systemctl', 'is-active', service_name], 
                              capture_output=True, text=True)
        is_active = result.stdout.strip() == 'active'
 
        status = subprocess.run(['systemctl', 'status', service_name], 
                              capture_output=True, text=True)
        
        if is_active:
            message = "Running"
            logging.info(f"Service {service_name} is running")
        else:
            message = "Stopped"
            logging.warning(f"Service {service_name} is not running: {status.stdout}")
        
        return is_active, message
        
    except Exception as e:
        logging.error(f"Error checking service status: {e}")
        return False, "Error"

font = {
    '0': [0x3E, 0x51, 0x49, 0x45, 0x3E],
    '1': [0x00, 0x42, 0x7F, 0x40, 0x00],
    '2': [0x42, 0x61, 0x51, 0x49, 0x46],
    '3': [0x21, 0x41, 0x45, 0x4B, 0x31],
    '4': [0x18, 0x14, 0x12, 0x7F, 0x10],
    '5': [0x27, 0x45, 0x45, 0x45, 0x39],
    '6': [0x3C, 0x4A, 0x49, 0x49, 0x30],
    '7': [0x01, 0x71, 0x09, 0x05, 0x03],
    '8': [0x36, 0x49, 0x49, 0x49, 0x36],
    '9': [0x06, 0x49, 0x49, 0x29, 0x1E],
    '.': [0x00, 0x60, 0x60, 0x00, 0x00],
    ':': [0x00, 0x36, 0x36, 0x00, 0x00],
    ' ': [0x00, 0x00, 0x00, 0x00, 0x00],
    'A': [0x7E, 0x11, 0x11, 0x11, 0x7E],
    'B': [0x7F, 0x49, 0x49, 0x49, 0x36],
    'C': [0x3E, 0x41, 0x41, 0x41, 0x22],
    'D': [0x7F, 0x41, 0x41, 0x22, 0x1C],
    'E': [0x7F, 0x49, 0x49, 0x49, 0x41],
    'F': [0x7F, 0x09, 0x09, 0x09, 0x01],
    'G': [0x3E, 0x41, 0x49, 0x49, 0x7A],
    'H': [0x7F, 0x08, 0x08, 0x08, 0x7F],
    'I': [0x00, 0x41, 0x7F, 0x41, 0x00],
    'J': [0x20, 0x40, 0x41, 0x3F, 0x01],
    'K': [0x7F, 0x08, 0x14, 0x22, 0x41],
    'L': [0x7F, 0x40, 0x40, 0x40, 0x40],
    'M': [0x7F, 0x02, 0x0C, 0x02, 0x7F],
    'N': [0x7F, 0x04, 0x08, 0x10, 0x7F],
    'O': [0x3E, 0x41, 0x41, 0x41, 0x3E],
    'P': [0x7F, 0x09, 0x09, 0x09, 0x06],
    'Q': [0x3E, 0x41, 0x51, 0x21, 0x5E],
    'R': [0x7F, 0x09, 0x19, 0x29, 0x46],
    'S': [0x46, 0x49, 0x49, 0x49, 0x31],
    'T': [0x01, 0x01, 0x7F, 0x01, 0x01],
    'U': [0x3F, 0x40, 0x40, 0x40, 0x3F],
    'V': [0x1F, 0x20, 0x40, 0x20, 0x1F],
    'W': [0x3F, 0x40, 0x38, 0x40, 0x3F],
    'X': [0x63, 0x14, 0x08, 0x14, 0x63],
    'Y': [0x07, 0x08, 0x70, 0x08, 0x07],
    'Z': [0x61, 0x51, 0x49, 0x45, 0x43],
    'a': [0x20, 0x54, 0x54, 0x54, 0x78],
    'b': [0x7F, 0x48, 0x44, 0x44, 0x38],
    'c': [0x38, 0x44, 0x44, 0x44, 0x20],
    'd': [0x38, 0x44, 0x44, 0x48, 0x7F],
    'e': [0x38, 0x54, 0x54, 0x54, 0x18],
    'f': [0x08, 0x7E, 0x09, 0x01, 0x02],
    'g': [0x0C, 0x52, 0x52, 0x52, 0x3E],
    'h': [0x7F, 0x08, 0x04, 0x04, 0x78],
    'i': [0x00, 0x44, 0x7D, 0x40, 0x00],
    'j': [0x20, 0x40, 0x44, 0x3D, 0x00],
    'k': [0x7F, 0x10, 0x28, 0x44, 0x00],
    'l': [0x00, 0x41, 0x7F, 0x40, 0x00],
    'm': [0x7C, 0x04, 0x18, 0x04, 0x78],
    'n': [0x7C, 0x08, 0x04, 0x04, 0x78],
    'o': [0x38, 0x44, 0x44, 0x44, 0x38],
    'p': [0x7C, 0x14, 0x14, 0x14, 0x08],
    'q': [0x08, 0x14, 0x14, 0x18, 0x7C],
    'r': [0x7C, 0x08, 0x04, 0x04, 0x08],
    's': [0x48, 0x54, 0x54, 0x54, 0x20],
    't': [0x04, 0x3F, 0x44, 0x40, 0x20],
    'u': [0x3C, 0x40, 0x40, 0x20, 0x7C],
    'v': [0x1C, 0x20, 0x40, 0x20, 0x1C],
    'w': [0x3C, 0x40, 0x30, 0x40, 0x3C],
    'x': [0x44, 0x28, 0x10, 0x28, 0x44],
    'y': [0x0C, 0x50, 0x50, 0x50, 0x3C],
    'z': [0x44, 0x64, 0x54, 0x4C, 0x44]
}

def wait_for_ip():
    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < CONFIG['IP_CHECK_TIMEOUT']:
        ip = get_ip_address()
        if ip:
            logging.info(f"IP found: {ip}")
            return ip
        
        clear_display()
        display_text("Getting IP", 0)
        display_text("Please wait", 2)
        
        time.sleep(CONFIG['IP_CHECK_INTERVAL'])
    
    logging.warning("IP check timeout")
    return "IP not found"

def format_display_line(label, value):

    return f"{label}{value}"

def main():
    try:
        init_oled()
        clear_display()
        
        last_ip_check = datetime.now()
        last_service_check = datetime.now()

        ip = wait_for_ip()
        service_status = "Checking"
        
        while True:
            current_time = datetime.now()
            
            if (current_time - last_ip_check).total_seconds() >= CONFIG['DISPLAY_UPDATE_INTERVAL']:
                new_ip = get_ip_address()
                if new_ip:
                    ip = new_ip
                last_ip_check = current_time
     
            if (current_time - last_service_check).total_seconds() >= CONFIG['SERVICE_CHECK_INTERVAL']:
                _, service_status = check_service_status(CONFIG['SERVICE_NAME'])
                last_service_check = current_time
            
            clear_display()
            
          
            display_text(format_display_line("IP:", ip if ip else "No IP"), 0)
            display_text(format_display_line("Server:", service_status), 2)
            
            time.sleep(30)  
            
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        if 'I/O error' in str(e):
            logging.error("Check your I2C connection and address")
        raise

if __name__ == "__main__":
    main()
