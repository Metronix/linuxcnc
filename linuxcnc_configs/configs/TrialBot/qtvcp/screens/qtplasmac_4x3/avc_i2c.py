import sys
import smbus2
from PyQt5 import QtCore, QtWidgets
from qtvcp.widgets.hal_label import HALLabel
from qtvcp.widgets.simple_widgets import DoubleScale, PushButton

class I2CCommunicator:
    def __init__(self, bus=1, address=0x55):
        self.bus_num = bus
        self.address = address
        self.bus = None
        self.connect()
        
    def connect(self):
        try:
            self.bus = smbus2.SMBus(self.bus_num)
            return True
        except Exception as e:
            print("Erro de conexão I2C:", e)
            return False
            
    def write_config(self, arc_voltage, dead_zone, max_volts):
        try:
            voltage_int = int(arc_voltage * 100)
            data = [
                (voltage_int >> 8) & 0xFF,
                voltage_int & 0xFF,
                int(dead_zone * 10),
                int(max_volts)
            ]
            self.bus.write_i2c_block_data(self.address, 0x04, data)
            return True
        except Exception as e:
            print("Erro na escrita:", e)
            self.connect()
            return False
            
    def read_config(self):
        try:
            self.bus.write_byte(self.address, 0x03)
            data = self.bus.read_i2c_block_data(self.address, 0x03, 4)
            voltage = ((data[0] << 8) | data[1]) / 100.0
            dead_zone = data[2] / 10.0
            max_voltage = data[3]
            return (voltage, dead_zone, max_voltage)
        except Exception as e:
            print("Erro na leitura:", e)
            self.connect()
            return None
            
    def read_voltage(self):
        try:
            self.bus.write_byte(self.address, 0x05)
            data = self.bus.read_i2c_block_data(self.address, 0x05, 2)
            voltage = ((data[0] << 8) | data[1]) / 100.0
            return voltage
        except Exception as e:
            print("Erro na leitura de tensão:", e)
            self.connect()
            return None

class AVCController(QtCore.QObject):
    update_ui = QtCore.pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.i2c = I2CCommunicator()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.read_voltage_loop)
        
    def start_voltage_reading(self):
        self.timer.start(100)  # 10 vezes por segundo
        
    def read_voltage_loop(self):
        voltage = self.i2c.read_voltage()
        if voltage is not None:
            self.update_ui.emit({'voltage': voltage})
            
    def read_config(self):
        config = self.i2c.read_config()
        if config:
            self.update_ui.emit({
                'target_voltage': config[0],
                'dead_zone': config[1],
                'max_voltage': config[2]
            })
            self.start_voltage_reading()
            
    def write_config(self, arc_voltage, dead_zone, max_volts):
        if self.i2c.write_config(arc_voltage, dead_zone, max_volts):
            self.start_voltage_reading()

class AVCMain(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AVC()
        self.ui.setupUi(self)
        self.controller = AVCController()
        self.setup_connections()
        self.controller.update_ui.connect(self.update_gui)
        
    def setup_connections(self):
        self.ui.ler_valores_config.clicked.connect(self.controller.read_config)
        self.ui.configurar_arc.clicked.connect(self.send_config)
        
    def send_config(self):
        arc_voltage = self.ui.arc_voltage_set.value()
        dead_zone = self.ui.dead_zone_arc_set.value()
        max_volts = self.ui.max_voltage_set.value()
        self.controller.write_config(arc_voltage, dead_zone, max_volts)
        
    def update_gui(self, data):
        if 'voltage' in data:
            self.ui.arc_voltage_read.setText(f"{data['voltage']:.2f}")
        if 'target_voltage' in data:
            self.ui.arc_voltage_set.setValue(data['target_voltage'])
        if 'dead_zone' in data:
            self.ui.dead_zone_arc.setValue(data['dead_zone'])
        if 'max_voltage' in data:
            self.ui.max_voltage_set.setValue(data['max_voltage'])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AVCMain()
    window.show()
    sys.exit(app.exec_())
