#!/usr/bin/python
#   This is a component of LinuxCNC
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from stdglue import *
import serial
import time
import linuxcnc
import hal


# Configurar a porta serial (substitua 'ttyAMA0' se necessário)
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

#h = hal.get_value("qtplasmac.led_thc_up")
#print(h)

# Função para enviar dados
def enviar_dados(dados):
	ser.write(str(dados).encode())  # Enviar dados como bytes
	print(f'Dados enviados: {dados}')

# Função para ler dados
def ler_dados():
	time.sleep(1)  # Aguarda para receber dados
	if ser.in_waiting > 0:
		dados_recebidos = ser.readline().decode('utf-8').rstrip()
		print(f'Dados recebidos: {dados_recebidos}')
	else:
		print('Nenhum dado recebido')


def rs232(self,**kwargs):
	"""Função chamada pelo LinuxCNC para enviar e ler dados via UART."""
	s = linuxcnc.stat()	
	s.poll()
	mensagem = int(kwargs.get('p'))
	if s.state == 2:
		try:
			enviar_dados(mensagem)  # Exemplo de envio
			ler_dados()  # Exemplo de leitura
			return 0  # Sucesso
		except Exception as e:
			print(f'Erro: {e}')
			return 1  # Falha

