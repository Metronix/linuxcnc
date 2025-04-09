import sys
from PyQt5.QtWidgets import QApplication, QWidget
from smbus2 import SMBus
from avc_1 import Ui_AVC  # Importa a interface gerada pelo PyQt5

class I2CController(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AVC()
        self.ui.setupUi(self)

        # Configuração inicial do barramento I2C
        self.i2c_bus = SMBus(1)  # Barramento I2C-1
        self.device_address = 0x55  # Endereço do dispositivo I2C

        # Conectar botões a funções
        self.ui.ler_valores_config.clicked.connect(self.read_configuration)
        self.ui.configurar_arc.clicked.connect(self.write_configuration)

    def read_configuration(self):
        try:
            # Comando para iniciar a leitura da configuração
            self.i2c_bus.write_byte(self.device_address, 3)

            # Ler os 4 bytes de resposta
            data = self.i2c_bus.read_i2c_block_data(self.device_address, 0, 4)

            # Interpretar os dados
            arc_voltage = (data[0] << 8 | data[1]) / 100.0
            dead_zone = data[2] / 10.0
            max_voltage = data[3]

            # Atualizar interface com os valores lidos
            self.ui.arc_voltage_read.setText(f"{arc_voltage:.2f}")
            self.ui.dead_zone_arc.setText(f"{dead_zone:.1f}")
            self.ui.max_arc_voltage.setText(f"{max_voltage:.1f}")
        except Exception as e:
            print(f"Erro ao ler configuração: {e}")

    def write_configuration(self):
        try:
            # Obter valores da interface
            arc_voltage = self.ui.arc_voltage_set.value()  # Float
            dead_zone = self.ui.dead_zone_arc_set.value()  # Float
            max_voltage = self.ui.max_voltage_set.value()  # Float

            # Converter para o formato esperado pelo dispositivo
            voltage_int = int(arc_voltage * 100)
            data = [
                (voltage_int >> 8) & 0xFF,  # MSB
                voltage_int & 0xFF,        # LSB
                int(dead_zone * 10),       # Dead zone
                int(max_voltage)           # Max voltage
            ]

            # Enviar dados para o dispositivo
            self.i2c_bus.write_i2c_block_data(self.device_address, 0, data)

            # Atualizar interface (opcional iniciar leitura de tensão)
            self.read_voltage()
        except Exception as e:
            print(f"Erro ao escrever configuração: {e}")

    def read_voltage(self):
        try:
            # Leitura contínua de tensão
            self.i2c_bus.write_byte(self.device_address, 5)
            data = self.i2c_bus.read_i2c_block_data(self.device_address, 0, 2)

            # Calcular tensão
            value = (data[0] << 8) | data[1]
            voltage = value / 100.0

            # Atualizar o label na interface
            self.ui.arc_voltage.setText(f"{voltage:.2f}")
        except Exception as e:
            print(f"Erro ao ler tensão: {e}")

    def closeEvent(self, event):
        # Fechar o barramento I2C ao sair
        self.i2c_bus.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = I2CController()
    window.show()
    sys.exit(app.exec_())
