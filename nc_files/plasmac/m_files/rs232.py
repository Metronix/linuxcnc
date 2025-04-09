#!/usr/bin/python
import sys
import serial
import time

# Configurar a porta serial (substitua 'ttyAMA0' se necessário)
ser = serial.Serial('/dev/serial0', baudrate=57600, timeout=1)
#,parity=serial.PARITY_EVEN

# Função para enviar dados
def enviar_dados(dados):
    ser.write(dados.encode())  # Enviar dados como bytes
    print(f'Dados enviados: {dados}')

# Função para ler dados
def ler_dados():
    time.sleep(3)  # Aguarda para receber dados
    if ser.in_waiting > 0:
        dados_recebidos = ser.readline().decode('utf-8').rstrip()
        print(f'Dados recebidos: {dados_recebidos}')
    else:
        print('Nenhum dado recebido')

# Função principal para o LinuxCNC chamar
def rs232(self,**kwargs):
    """Função chamada pelo LinuxCNC para enviar e ler dados via UART."""
    global ser
    try:
        '''enviar_dados(('60')) # Exemplo de envio
        enviar_dados(('69'))  # Exemplo de envio
        enviar_dados(('7'))  # Exemplo de envio
        enviar_dados(('0'))  # Exemplo de envio'''
        #ser.write(bytes([255,255,255,255]))
        #dados_recebidos = ser.readline()
        #print(f'Dados recebidos: {dados_recebidos}')
        ser.write(bytes([60,69,6,0]))
        dados_recebidos = ser.readline()
        print(f'Dados recebidos2: {dados_recebidos}')
        #ser.write(bytes([60,69,7,0]))
        #ler_dados()  # Exemplo de leitura
        return 0  # Sucesso
    except Exception as e:
        print(f'Erro: {e}')
        return 1  # Falha

