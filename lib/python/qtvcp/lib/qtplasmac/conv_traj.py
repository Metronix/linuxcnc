'''
conv_traj.py

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

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QLabel, QMessageBox
from importlib import reload
from plasmac import traj as TRAJ

_translate = QCoreApplication.translate

def preview(P, W, Conv):
    if P.dialogError:
        return
    if not W.xsEntry.text():
        W.xsEntry.setText('{:0.3f}'.format(P.xOrigin))
    if not W.ysEntry.text():
        W.ysEntry.setText('{:0.3f}'.format(P.yOrigin))
    origin = W.centLeft.text() == 'CENTER'
    error = TRAJ.preview(W, Conv, P.fTmp, P.fNgc, P.fNgcBkp, \
            int(W.conv_material.currentText().split(':')[0]), \
            W.conv_material.currentText().split(':')[1].strip(), \
            P.preAmble, P.postAmble, \
            W.xsEntry.text(), W.ysEntry.text(), \
            W.dsEntry.text(), W.velEntry.text(), \
            W.ampEntry.text(), W.freqEntry.text(), W.tp1Entry.text(), \
            W.tp2Entry.text(), W.tdispEntry.text(), W.dirCheck.isChecked())
    if error:
        P.dialogError = True
        P.dialog_show_ok(QMessageBox.Warning, _translate('Conversational', 'Star Error'), error)
    else:
        W.conv_preview.load(P.fNgc)
        W.conv_preview.set_current_view()
        W.add.setEnabled(True)
        W.undo.setEnabled(True)
        Conv.conv_preview_button(P, W, True)

def auto_preview(P, W, Conv, button=False):
    if button == 'intext':
        if not W.intExt.isChecked():
            return
        Conv.conv_auto_preview_button(P, W, button)
    elif button == 'center':
        if not W.centLeft.isChecked():
            return
        Conv.conv_auto_preview_button(P, W, button)
    if W.main_tab_widget.currentIndex() == 1 and \
       W.pEntry.text() and W.odEntry.text() and W.idEntry.text():
        preview(P, W, Conv)

def entry_changed(P, W, Conv, widget):
    Conv.conv_entry_changed(P, W, widget)

def widgets(P, W, Conv):
    if P.developmentPin.get():
        reload(TRAJ)
    W.lDesc.setText(_translate('Conversational', 'CREATING TRAJECTORY'))
    W.iLabel.setPixmap(P.conv_star_l)
    #alignment and size
    rightAlign = ['xsLabel', 'xsEntry', 'ysLabel', \
                  'ysEntry', 'dsLabel', 'dsEntry', \
                  'velLabel', 'velEntry', 'ampLabel', \
                  'ampEntry', 'freqLabel', 'freqEntry', \
                  'dirLabel', 'tp1Label', 'tp1Entry', 'tp2Label', 'tp2Entry', 'tdispLabel', 'tdispEntry']
                  
                 
    centerAlign = ['lDesc']
    rButton = ['intExt', 'centLeft']
    pButton = ['preview', 'add', 'undo']
    for widget in rightAlign:
        W[widget].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        W[widget].setFixedWidth(90)
        W[widget].setFixedHeight(24)
    for widget in centerAlign:
        W[widget].setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        W[widget].setFixedWidth(240)
        W[widget].setFixedHeight(24)
    for widget in rButton:
        W[widget].setFixedWidth(80)
        W[widget].setFixedHeight(24)
    for widget in pButton:
        W[widget].setFixedWidth(80)
        W[widget].setFixedHeight(24)
    #connections
    W.conv_material.currentTextChanged.connect(lambda:auto_preview(P, W, Conv))
    W.intExt.toggled.connect(lambda:auto_preview(P, W, Conv, 'intext'))
    W.centLeft.toggled.connect(lambda:auto_preview(P, W, Conv, 'center'))
    W.preview.pressed.connect(lambda:preview(P, W, Conv))
    W.add.pressed.connect(lambda:Conv.conv_add_shape_to_file(P, W))
    W.undo.pressed.connect(lambda:Conv.conv_undo_shape(P, W))
    entries = ['xsEntry', 'ysEntry', 'dsEntry', 'velEntry', \
               'ampEntry', 'freqEntry', 'velEntry', 'tp1Entry', 'tp2Entry', 'tdispEntry']
    for entry in entries:
        W[entry].textChanged.connect(lambda:entry_changed(P, W, Conv, W.sender()))
        W[entry].returnPressed.connect(lambda:preview(P, W, Conv))
    #add to layout
    if P.landscape:
        text = _translate('Conversational', 'START')
        W.xsLabel.setText(_translate('Conversational', 'X {}'.format(text)))
        W.entries.addWidget(W.xsLabel, 0, 0)
        W.entries.addWidget(W.xsEntry, 0, 1)
        W.ysLabel.setText(_translate('Conversational', 'Y {}'.format(text)))
        W.entries.addWidget(W.ysLabel, 1, 0)
        W.entries.addWidget(W.ysEntry, 1, 1)
        W.entries.addWidget(W.dsLabel, 2, 0)
        W.entries.addWidget(W.dsEntry, 2, 1)
        W.entries.addWidget(W.velLabel, 3, 0)
        W.entries.addWidget(W.velEntry, 3, 1)
        W.entries.addWidget(W.ampLabel, 4, 0)
        W.entries.addWidget(W.ampEntry, 4, 1)
        W.entries.addWidget(W.freqLabel, 5, 0)
        W.entries.addWidget(W.freqEntry, 5, 1)
        W.entries.addWidget(W.tp1Label, 6, 0)
        W.entries.addWidget(W.tp1Entry, 6, 1)
        W.entries.addWidget(W.tp2Label, 7, 0)
        W.entries.addWidget(W.tp2Entry, 7, 1)
        W.entries.addWidget(W.tdispLabel, 8, 0)
        W.entries.addWidget(W.tdispEntry, 8, 1)
        W.entries.addWidget(W.dirLabel, 9, 0)
        W.entries.addWidget(W.dirCheck, 9, 1)
        
        for r in [10,11]:
            W['s{}'.format(r)] = QLabel('')
            W['s{}'.format(r)].setFixedHeight(24)
            W.entries.addWidget(W['s{}'.format(r)], r, 0)
        W.entries.addWidget(W.preview, 12, 0)
        W.entries.addWidget(W.add, 12, 2)
        W.entries.addWidget(W.undo, 12, 4)
        W.entries.addWidget(W.lDesc, 13 , 1, 1, 3)
        W.entries.addWidget(W.iLabel, 0 , 2, 7, 3)
    else:
        W.entries.addWidget(W.conv_material, 0, 0, 1, 5)
        W.entries.addWidget(W.xsLabel, 3, 0)
        W.entries.addWidget(W.xsEntry, 3, 1)
        W.entries.addWidget(W.ysLabel, 3, 2)
        W.entries.addWidget(W.ysEntry, 3, 3)
        W.entries.addWidget(W.dsLabel, 3, 4)
        W.entries.addWidget(W.dsEntry, 3, 5)
        W.entries.addWidget(W.velLabel, 3, 6)
        W.entries.addWidget(W.velEntry, 3, 7)
        W.entries.addWidget(W.ampLabel, 3, 8)
        W.entries.addWidget(W.ampEntry, 3, 9)
        W.entries.addWidget(W.freqLabel, 3, 10)
        W.entries.addWidget(W.freqEntry, 3, 11)
        W.entries.addWidget(W.dirLabel, 3, 12)
        W.entries.addWidget(W.dirCheck, 3, 13)
        W.s8 = QLabel('')
        W.s8.setFixedHeight(24)
        W.entries.addWidget(W.s8, 8, 0)
        W.entries.addWidget(W.preview, 9, 0)
        W.entries.addWidget(W.add, 9, 2)
        W.entries.addWidget(W.undo, 9, 4)
        W.entries.addWidget(W.lDesc, 10 , 1, 1, 3)
        W.entries.addWidget(W.iLabel, 0 , 5, 7, 3)
    W.pEntry.setFocus()
    P.convSettingsChanged = False
