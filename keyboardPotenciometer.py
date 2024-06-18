import serial
import pyautogui
import time

# Função para abrir a porta serial
def open_serial_port(port, baudrate):
    try:
        ser = serial.Serial(port, baudrate)
        time.sleep(2)  # Tempo para garantir que a conexão serial está estabelecida
        return ser
    except serial.SerialException as e:
        print(f"Erro ao abrir porta serial: {e}")
        return None

# Porta serial correta
serial_port = '/dev/ttyUSB0'  # Substitua '/dev/ttyUSB0' pela sua porta serial
baud_rate = 9600

ser = open_serial_port(serial_port, baud_rate)

if ser is None:
    exit("Falha ao abrir a porta serial. Verifique a conexão e as permissões.")

current_key = None
last_line = ""  # Variável para armazenar a última mensagem recebida
last_seen = time.time()  # Timestamp da última vez que uma mensagem foi recebida

# Duração para manter a tecla pressionada (em segundos)
KEY_PRESS_DURATION = 0.5 #Aumentei para 0.5 segundos

# Margem de histerese para reduzir sensibilidade a mudanças pequenas
HISTERESIS_MARGIN = 50

while True:
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Recebido: {line}")

            # Verificar se houve uma mudança significativa no sinal recebido
            if line != last_line:
                if (line == "LEFT" and current_key != "left") or (line == "RIGHT" and current_key != "right"):
                    if current_key is not None:
                        pyautogui.keyUp(current_key)

                    if line == "LEFT":
                        pyautogui.keyDown("left")
                        current_key = "left"
                    elif line == "RIGHT":
                        pyautogui.keyDown("right")
                        current_key = "right"

                last_line = line
                last_seen = time.time()

        # Verificar se o potenciômetro parou de ser girado
        if time.time() - last_seen > KEY_PRESS_DURATION + HISTERESIS_MARGIN / 1000.0 and current_key is not None:
            pyautogui.keyUp(current_key)
            current_key = None

    except serial.SerialException as e:
        print(f"Erro durante a leitura da porta serial: {e}")
        break
    except Exception as e:
        print(f"Erro inesperado: {e}")
        break

ser.close()
