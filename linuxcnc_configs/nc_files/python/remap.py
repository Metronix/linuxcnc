#!/usr/bin/python
import sys
import serial
import time
from interpreter import *
from util import lineno


ser = serial.Serial('/dev/serial0', baudrate=57600, timeout=1)

# Configurar a porta serial (substitua 'ttyAMA0' se necessário)

#,parity=serial.PARITY_EVEN
"""
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
""""""
def rs232(self,**kwargs):
    Função chamada pelo LinuxCNC para enviar e ler dados via UART.
    global ser
    try:
        '''enviar_dados(('60')) # Exemplo de envio
        enviar_dados(('69'))  # Exemplo de envio
        enviar_dados(('7'))  # Exemplo de envio
        enviar_dados(('0'))  # Exemplo de envio'''
        ser.write(bytes([255,255,255,255]))
        dados_recebidos = ser.readline()
        #print(f'Dados recebidos: {dados_recebidos}')
        #time.sleep(1)
        
        ser.write(bytes([99,69,7,0]))
        dados_recebidos = ser.readline()
        
        return 0  # Sucesso
    except Exception as e:
        print(f'Erro: {e}')
        return 1  # Falha
    
"""
"""
def liga(self,**words):
    try:
        #P = words['P']
        ser.write(bytes([255,255,255,255]))
        dados_recebidos = ser.readline()
        
        ser.write(bytes([60,69,7,0]))
        dados_recebidos = ser.readline()
        #self.execute("G04%f" % P)
        #print(f'Dados recebidos2: {dados_recebidos}')
        return 0  # Sucesso
    except Exception as e:
        print(f'Erro: {e}')
        return 1  # Falha
""""""
def desliga(self,**kwargs):
    try:
        
        ser.write(bytes([255,255,255,255]))
        dados_recebidos = ser.readline()
        #print(f'Dados recebidos: {dados_recebidos}')
        #time.sleep(1)
        ser.write(bytes([60,69,6,0]))
        dados_recebidos = ser.readline()
        print(f'Dados recebidos2: {dados_recebidos}')
        return 0  # Sucesso
    except Exception as e:
        print(f'Erro: {e}')
        return 1  # Falha
"""
def rs232(self, **words): 
    
    if self.task:
        try: 
            yield INTERP_EXECUTE_FINISH  
            if words['p'] == 1: 
                ser.write(bytes([255,255,255,255])) 
                ser.write(bytes([99,60,48,0])) 
                
            elif words['p'] == 2:
                ser.write(bytes([255,255,255,255])) 
                ser.write(bytes([99,60,49,0])) 
            elif words['p'] == 3:
                ser.write(bytes([255,255,255,255])) 
                ser.write(bytes([99,60,50,0])) 
            #dados_recebidos = ser.readline()
            #print(f'Dados recebidos: {dados_recebidos}')
        except Exception as e:
            print(f'Erro: {e}')  
    yield INTERP_EXECUTE_FINISH                 
    return INTERP_OK

def liga(self, **words): 
    # Se estiver em simulação (preview), não executa os comandos de hardware: 
    
    if self.task:
        try:
            #self.execute("M3",lineno())
            #self.execute("G04 P%f" % words['p'], lineno())
            yield INTERP_EXECUTE_FINISH  
            ser.write(bytes([255,255,255,255])) 
            ser.write(bytes([60,69,7,0])) 
        except Exception as e: 
            print(f'Erro: {e}')
    yield INTERP_EXECUTE_FINISH  
    return INTERP_OK   

def desliga(self, **words): 
    
    if self.task:
        try: 
            #self.execute("M5",lineno())
            yield INTERP_EXECUTE_FINISH 
            ser.write(bytes([255,255,255,255])) 
            ser.write(bytes([60,69,6,0])) 
        except Exception as e: 
            print(f'Erro: {e}') 
    yield INTERP_EXECUTE_FINISH   
    return INTERP_OK 

