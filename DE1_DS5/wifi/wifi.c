#include <stdio.h>
#include <string.h>
#include <time.h>
//...............................................................................................
#define Wifi_ReceiverFifo        				(*(volatile unsigned char *)(0xFF210210))
#define Wifi_TransmitterFifo     				(*(volatile unsigned char *)(0xFF210210))
#define Wifi_InterruptEnableReg  				(*(volatile unsigned char *)(0xFF210212))
#define Wifi_InterruptIdentificationReg 			(*(volatile unsigned char *)(0xFF210214))
#define Wifi_FifoControlReg 						(*(volatile unsigned char *)(0xFF210214))
#define Wifi_LineControlReg 						(*(volatile unsigned char *)(0xFF210216))
#define Wifi_ModemControlReg 					(*(volatile unsigned char *)(0xFF210218))
#define Wifi_LineStatusReg 						(*(volatile unsigned char *)(0xFF21021A))
#define Wifi_ModemStatusReg 						(*(volatile unsigned char *)(0xFF21021C))
#define Wifi_ScratchReg 							(*(volatile unsigned char *)(0xFF21021E))
#define Wifi_DivisorLatchLSB 					(*(volatile unsigned char *)(0xFF210210))
#define Wifi_DivisorLatchMSB 					(*(volatile unsigned char *)(0xFF210212))

void init_Wifi(void) {
	// set bit 7 of Line Control Register to 1, to gain access to the baud rate registers
	unsigned char line_control_register= Wifi_LineControlReg;
	line_control_register = line_control_register |  0x80;
	Wifi_LineControlReg= line_control_register;
	// set Divisor latch (LSB and MSB) with correct value for required baud rate
	int divisor = (int) ((50E6)/(112500 *16));
	Wifi_DivisorLatchLSB = divisor & 0xff;
	Wifi_DivisorLatchMSB = (divisor >> 8) & 0xff;

	// set bit 7 of Line control register back to 0 and
	// program other bits in that reg for 8 bit data,
	// 1 stop bit, no parity etc
	Wifi_LineControlReg= 0x03;
	// Reset the Fifo’s in the FiFo Control Reg by setting bits 1 & 2
	Wifi_FifoControlReg = Wifi_FifoControlReg | 0x06;
	// Now Clear all bits in the FiFo control registers
	Wifi_FifoControlReg = Wifi_FifoControlReg ^  0x06;
}

int putcharWifi(int c) {
    while((Wifi_LineStatusReg & 0x20)!= 0x20){}
    Wifi_TransmitterFifo = c;
    return c;
}

void putstringWifi(char* string){
    int i;
    for(i = 0; i < strlen(string); i++){
        putcharWifi(string[i]);
    }
    putcharWifi('\r');
    putcharWifi('\n');
}

int getcharWifi(void) {
	while ((Wifi_LineStatusReg & 0x01)!= 0x01);
	return (int) Wifi_ReceiverFifo;
}

void getstringWifi(volatile char* buff){
    buff[0] = getcharWifi();
    volatile int i = 1;
    while ((Wifi_LineStatusReg & 1)){
        buff[i] = Wifi_ReceiverFifo;
        i++;
        }
    buff[i] = '\0';
}

int WifiTestForReceivedData(void) {
	if((Wifi_LineStatusReg & 0x01)== 0x01){
		return 1;
	}
	else{
		return 0;
	}
}

void WifiFlush(void) {
    volatile int dummy = 0;
    while(Wifi_LineStatusReg & 1) {
        dummy += Wifi_ReceiverFifo;
    }
    return;
}

void main(){
    init_Wifi();
    // enter the lua mode
    putcharWifi('\r');
    putcharWifi('\n');

    // send a GET request
    putstringWifi("wifi.sta.config('TP-LINK_888','12345687')");
    putstringWifi("wifi.sta.connect()");
    putstringWifi("tmr.delay(1000000)");
    putstringWifi("sk=net.createConnection(net.TCP, 0)");
    putstringWifi("sk:on('receive', function(sck, c) print(c) end )");
    putstringWifi("sk:connect(3000,'52.138.39.36')");
    putstringWifi("sk:send('GET /ws\r\nConnection: keep-alive\r\nAccept: */*\r\n\r\n')");

    volatile char Char = getcharWifi();
    printf("received %c\n", Char);
    WifiFlush();

    while(1){}
}
