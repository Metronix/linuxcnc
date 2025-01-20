'''
traj.py

Copyright (C) 2020, 2021, 2022  Phillip A Carter
Copyright (C) 2020, 2021, 2022  Gregory D Carl

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

import os
import sys
import math
import gettext
from PyQt5.QtWidgets import QMessageBox, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import Qt


for f in sys.path:
    if '/lib/python' in f:
        if '/usr' in f:
            localeDir = 'usr/share/locale'
        else:
            localeDir = os.path.join('{}'.format(f.split('/lib')[0]),'share','locale')
        break
gettext.install("linuxcnc", localedir=localeDir)

# Conv is the upstream calling module
def preview(W ,Conv, fTmp, fNgc, fNgcBkp, \
            matNumber, matName, \
            preAmble, postAmble, \
            xStart, yStart, \
            dist, vs, amp, \
            frq, tp1, tp2, tdisp, dir):
    
    
    error = ''
    msg1 = _('entry is invalid')
    valid, xStart = Conv.conv_is_float(xStart)
    if not valid and xStart:
        msg0 = _('X START')
        error += '{} {}\n\n'.format(msg0, msg1)
    valid, yStart = Conv.conv_is_float(yStart)
    if not valid and yStart:
        msg0 = _('Y Start')
        error += '{} {}\n\n'.format(msg0, msg1)
    valid, dist = Conv.conv_is_float(dist)
    if not valid and dist:
        msg0 = _('Distância')
        error += '{} {}\n\n'.format(msg0, msg1)
    valid, vs = Conv.conv_is_float(vs)
    if not valid and vs:
        msg0 = _('Velocidade')
        error += '{} {}\n\n'.format(msg0, msg1)
    valid, amp = Conv.conv_is_float(amp)
    if not valid and amp:
        msg0 = _('Amplitude')
        error += '{} {}\n\n'.format(msg0, msg1)
    valid, frq = Conv.conv_is_float(frq)
    if not valid and frq:
        msg0 = _('Frequência')
        error += '{} {}\n\n'.format(msg0, msg1)
    valid, tp1 = Conv.conv_is_float(tp1)
    if not valid and tp1:
        msg0 = _('Tempo de parada 1')
        error += '{} {}\n\n'.format(msg0, msg1)
    valid, tp2 = Conv.conv_is_float(tp2)
    if not valid and tp2:
        msg0 = _('Tempo de parada 2')
        error += '{} {}\n\n'.format(msg0, msg1)
    valid, tdisp = Conv.conv_is_float(tdisp)
    
    
    if not valid:
        msg = _('Tempo de disparo inválido')
        error += '{}\n\n'.format(msg)
    if error:
        return error
    if dist <= 0:
        msg = _('Distância precisa ser > 0')
        error += '{}\n\n'.format(msg)
    if vs <= 0:
        msg = _('Velocidade não pode ser menor que zero')
        error += '{}\n\n'.format(msg)
    if tp2 < 0:
        msg = _('Tempo de parada 2 não pode ser menor que zero')
        error += '{}\n\n'.format(msg)
    if tp1 < 0:
        msg = _('Tempo de parada 1 não pode ser menor que zero')
        error += '{}\n\n'.format(msg)
    if frq > 5 or frq <= 0:
        msg = _('Frequência maior/menor que a permitida')
        error += '{}\n\n'.format(msg)
    if amp > 11:
        msg = _('Amplitude maior que a permitida')
        error += '{}\n\n'.format(msg)
    if error:
        return error
    if dir == 0:
        dir = -1
    
    aMax = 60*(1/frq -tp1 -tp2)
    fMax = 1/((2*amp/60) +tp1 +tp2)
    tSupMax = -(2*amp/60) +(1/frq) - tp2
    tInfMax = -(2*amp/60) +(1/frq) - tp1
    
    W.aMax = QLabel(f'Amplitude Max: {aMax:.2f}')
    W.entries.addWidget(W.aMax, 16 , 0, 1, 3)
    
    W.fMax = QLabel(f'Frequência Max: {fMax:.2f}')
    W.entries.addWidget(W.fMax, 17 , 0, 1, 3)
    
    W.tSupMax = QLabel(f'Tempo superior Max: {tSupMax:.2f}')
    W.entries.addWidget(W.tSupMax, 18 , 0, 1, 3)
    
    W.tInfMax = QLabel(f'Tempo inferior Max: {tInfMax:.2f}')
    W.entries.addWidget(W.tInfMax, 19 , 0, 1, 3)   
    
    rightAlign = ['aMax', 'fMax', 'tSupMax', 'tInfMax']
    for widget in rightAlign: 
        W[widget].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        W[widget].setStyleSheet("font-size: 18px")
        W[widget].adjustSize()
    
    
    outTmp = open(fTmp, 'w')
    outNgc = open(fNgc, 'w')
    inWiz = open(fNgcBkp, 'r')
    for line in inWiz:
        if '(new conversational file)' in line:
            if('\\n') in preAmble:
                outNgc.write('(preamble)\n')
                for l in preAmble.split('\\n'):
                    outNgc.write('{}\n'.format(l))
            else:
                outNgc.write('\n{} (preamble)\n'.format(preAmble))
            break
        elif '(postamble)' in line:
            break
        elif 'm2' in line.lower() or 'm30' in line.lower():
            continue
        outNgc.write(line)
    outTmp.write(f'\n#<tube-cut>=1\n')
    outTmp.write('\n(conversational trajectory {})\n')
    #outTmp.write(';using material #{}: {}\n'.format(matNumber, matName))
    #outTmp.write('M190 P{}\n'.format(matNumber))
    #outTmp.write('M66 P3 L3 Q1\n')
    #outTmp.write('f#<_hal[plasmac.cut-feed-rate]>\n')
        
    periodo = 1 / frq
    velocidadeX = vs / 6
    distanciaPeriodo = velocidadeX * periodo
    distanciaUmMeioX = distanciaPeriodo / 2
    distanciaUmQuartoX = distanciaPeriodo / 4
    distanciaY = amp  # Componente da Amplitude no eixo Y
    distanciaUmMeioY = distanciaY / 2
    distanciaHipotenusa = math.sqrt(distanciaUmQuartoX**2 + distanciaUmMeioY**2)
    velocidadeHipotenusa = round(((distanciaHipotenusa * 4) / (periodo - (tp1 + tp2))) * 60, 2)
    repeticoes = round((dist - distanciaPeriodo) / distanciaPeriodo)
    resto = dist - (repeticoes * distanciaPeriodo + distanciaUmMeioX)
    if velocidadeHipotenusa > 4000:
        msg = _('Tempo de parada maior que o permitido\n (velocidade entre pontos muito grande)')
        error += '{}\n\n'.format(msg)
    if tp1 + tp2 >= periodo*0.8:
        msg = _('Tempo de parada maior que o permitido')
        error += '{}\n\n'.format(msg)
    if error:
        return error
    # Geração do código
    outTmp.write(f"( VelocidadeSoldagem = {vs} cm/min )\n")
    outTmp.write(f"( Amplitude = {amp} mm )\n")
    outTmp.write(f"( Frequencia = {frq} Hz )\n")
    outTmp.write(f"( Tempo de Parada 1 = {tp1} s )\n")
    outTmp.write(f"( Tempo de Parada 2 = {tp2} s )\n")
    outTmp.write(f"( Tempo de Disparo = {tdisp} s )\n")
    outTmp.write(f"( Distância total = {dist} mm )\n")
    outTmp.write(f"( Direção = {dir} )\n")

    #outTmp.write("G0 G49 G40 G17 G80 G50 G90")
    outTmp.write(f"G0 X{xStart} Y{yStart}\n")
    outTmp.write(f"G01 G90 F{velocidadeHipotenusa}\n")
    #outTmp.write(f"G04 P1")
    if tdisp > 0:
        outTmp.write(f"M200 P{tdisp}\n")
    else:
        outTmp.write(f"M200 P{0}\n")

    outTmp.write(f"( Repeticoes = {repeticoes} )\n")
    outTmp.write(f"( Resto = {resto} mm )\n")
    outTmp.write(f"( Cordao principal - Distancia = {repeticoes * distanciaPeriodo + distanciaUmMeioX} mm )\n")
    
    #inicio
    outTmp.write(f"G1 G91 X{dir * distanciaUmQuartoX} Y{distanciaUmMeioY} F{velocidadeHipotenusa}\n")
    
    #repeticoes
    outTmp.write(f"(Repeticoes = {repeticoes})\n")
    i = repeticoes // 500
    for j in range(1, i + 1):
        outTmp.write("M98 P0001 L500\n")
    outTmp.write(f"M98 P0001 L{repeticoes - i * 500}\n")
    
    #final
    outTmp.write(f"G1 X{dir * distanciaUmQuartoX} Y{-distanciaUmMeioY} F{velocidadeHipotenusa}\n")
    
    outTmp.write(f"(Resto = {resto} mm)\n")    
    outTmp.write(f"G1 X{dir * resto} F{velocidadeHipotenusa}\n")

    outTmp.write("M30\n")
    
    # Código adicional do Visual Basic convertido para Python
    outTmp.write("O0001\n")    
    # Aplica o tempo de parada 1
    if tp1 > 0:
        outTmp.write(f"G4 P{tp1}\n")    
    # Realiza primeira metade do tecimento
    outTmp.write(f"G1 X{dir * distanciaUmMeioX} Y{-distanciaY} F{velocidadeHipotenusa}\n")    
    # Aplica o tempo de parada 2
    if tp2 > 0:
        outTmp.write(f"G4 P{tp2}\n")    
    # Realiza segunda metade do tecimento
    outTmp.write(f"G1 X{dir * distanciaUmMeioX} Y{distanciaY} F{velocidadeHipotenusa}\n")    
    # Fim do loop
    outTmp.write("M99\n")
    if tdisp > 0:
        outTmp.write(f"M200 P{tdisp}\n")
    else:
        outTmp.write(f"M200 P{0}\n")
    #outTmp.write('m5 $0\n')
    outTmp.close()
    outTmp = open(fTmp, 'r')
    for line in outTmp:
        outNgc.write(line)
    outTmp.close()
    if('\\n') in postAmble:
        outNgc.write('(postamble)\n')
        for l in postAmble.split('\\n'):
            outNgc.write('{}\n'.format(l))
    else:
        outNgc.write('\n{} (postamble)\n'.format(postAmble))
    outNgc.write('m2\n')
    outNgc.close()
    return False


