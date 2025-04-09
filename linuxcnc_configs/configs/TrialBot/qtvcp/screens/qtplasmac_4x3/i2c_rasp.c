
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>
#include <stdbool.h>

bool thc_enable;                  //"enable/disable thc and set the IHS skip type";
float arc_voltage_in;              //"arc voltage input";
float max_volts;                   //"max voltage avc(volts)";
float dead_zone;
unsigned int state_handler;               //"set state";
bool bit    shutdown;


// Output Pins
float  voltage_out;
float  voltage;
float  dead_zone_out;
float  max_voltage_out;
unsigned int error_handler;

/* VARIABLES */

int16_t value;
int flag_conection = 0;
int state_handler_old = 0;
int device_addr = 0x55; // Endereço do dispositivo
int i2c_fd;
unsigned char buf[2];
unsigned char data[4];
const char *device = "/dev/i2c-1"; // Barramento I2C

enum states{
    IDLE = 0,
    THC_OFF,
    THC_ON,
    LER_CONFIG,
    GRAVAR,
    TENSAO  
};

enum states Estados= IDLE;

int connection(){
    // Abrir o barramento I2C
    if ((i2c_fd = open(device, O_RDWR)) < 0) {
        perror("Failed to open the I2C bus");
        return 1;
    }
    // Configurar o endereço do dispositivo
    if (ioctl(i2c_fd, I2C_SLAVE, device_addr) < 0) {
        perror("Failed to acquire bus access and/or talk to slave");
        close(i2c_fd);
        return 1;
    }
    return 0;
}
int main(){
    while(1){
        if (flag_conection == 0) {
            error_handler = connection();
            flag_conection = (error_handler == 0) ? 1 : 0; 
        }
        if(state_handler_old != state_handler){
            switch (state_handler){
                case 1:
                    Estados = THC_OFF;
                    break;
                case 3:
                    Estados = LER_CONFIG;
                    break;
                case 4:
                    Estados = GRAVAR;
                    break;
                case 5:
                    Estados = TENSAO;
                    break;
                default: 
                    break;
            }
            state_handler_old = state_handler;
        }
        switch (Estados){
            case IDLE:
                
                if(thc_enable){
                    Estados = THC_ON;
                }
                break;
            case THC_OFF:
                data[0] = 1;
                if(write(i2c_fd, data, 1) != 1){
                    perror("Failed to write to the I2C device");
                }
                Estados = IDLE;
                break;
            case THC_ON:
                data[0] = 2;
                if(write(i2c_fd, data, 1) != 1){
                    perror("Failed to write to the I2C device");
                }
                Estados = TENSAO;
                break;
            case LER_CONFIG:
                data[0] = 3;
                if(write(i2c_fd, data, 1) != 1){
                    perror("Failed to write to the I2C device");
                }
                if (read(i2c_fd, data, 4) != 4) {
                    perror("Failed to read from the I2C device");
                    close(i2c_fd);
                    flag_conection = 0;
                    Estados = THC_OFF;
                }else{
                    value = (data[0] << 8) | data[1]; // MSB no último byte
                    voltage_out = value / 100.0;
                    dead_zone_out = data[2]/10.0;
                    max_voltage_out = data[3];
                    //printf("Voltage: %.2f V\n", voltage);
                    //printf("Zona Morta: %.2f V\n",  data[2]/10.0);
                    //printf("Max Voltage: %.2f V\n", data[3]/1.0);
                    Estados = TENSAO;
                }
                break;
            case GRAVAR: 
                int16_t voltage_int = (int16_t)(arc_voltage_in * 100.0);
                data[0] =  (uint8_t)((voltage_int >> 8) & 0xFF); // MSB (byte mais significativo)
                data[1] =  (uint8_t)(voltage_int) & 0xFF;        // LSB (byte menos significativo)
                data[2] = (uint8_t)(dead_zone * 10.0);
                data[3] = (uint8_t)(max_volts);
                if(write(i2c_fd, data, sizeof(data)) != sizeof(data)){
                    perror("Failed to write to the I2C device");
                    flag_conection = 0;
                    Estados = THC_OFF;
                }else{
                    Estados = TENSAO;
                }
                break;
            case TENSAO:
                if (read(i2c_fd, buf, 2) != 2) {
                    perror("Failed to read from the I2C device");
                    close(i2c_fd);
                    flag_conection = 0;
                    Estados = THC_OFF;
                    break;
                }
                 value = (buf[0] << 8) | buf[1]; // MSB no último byte
                 voltage = value / 100.0;
                if(!thc_enable){
                    Estados = THC_OFF;
                }
                
                usleep(50000);
                break;
        }
          
        
        // Fechar o barramento
        if (shutdown) {
            close(i2c_fd);
            flag_conection = 0; // Reset para reconexão
        }
    }
}


