#include <stdio.h>
#include <time.h>
#include <math.h>

#define SWITCHES    (volatile unsigned int *)(0xFF200000)
#define PUSHBUTTONS (volatile unsigned int *)(0xFF200010)

#define LEDS        (volatile unsigned int *)(0xFF200020)
#define HEX0_1      (volatile unsigned int *)(0xFF200030)
#define HEX2_3      (volatile unsigned int *)(0xFF200040)
#define HEX4_5      (volatile unsigned int *)(0xFF200050)
//----------------------------------------------------------------------------------------------
#define RS232_ReceiverFifo         				(*(volatile unsigned char *)(0xFF210200))
#define RS232_TransmitterFifo      				(*(volatile unsigned char *)(0xFF210200))
#define RS232_InterruptEnableReg   				(*(volatile unsigned char *)(0xFF210202))
#define RS232_InterruptIdentificationReg        (*(volatile unsigned char *)(0xFF210204))
#define RS232_FifoControlReg                    (*(volatile unsigned char *)(0xFF210204))
#define RS232_LineControlReg                    (*(volatile unsigned char *)(0xFF210206))
#define RS232_ModemControlReg                   (*(volatile unsigned char *)(0xFF210208))
#define RS232_LineStatusReg                     (*(volatile unsigned char *)(0xFF21020A))
#define RS232_ModemStatusReg                    (*(volatile unsigned char *)(0xFF21020C))
#define RS232_ScratchReg                        (*(volatile unsigned char *)(0xFF21020E))

#define RS232_DivisorLatchLSB                   (*(volatile unsigned char *)(0xFF210200))
#define RS232_DivisorLatchMSB                   (*(volatile unsigned char *)(0xFF210202))
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
//................................................................................................
#define Bluetooth_ReceiverFifo        			((volatile unsigned char *)(0xFF210220))
#define Bluetooth_TransmitterFifo     			((volatile unsigned char *)(0xFF210220))
#define Bluetooth_InterruptEnableReg  			((volatile unsigned char *)(0xFF210222))
#define Bluetooth_InterruptIdentificationReg 	((volatile unsigned char *)(0xFF210224))
#define Bluetooth_FifoControlReg 				((volatile unsigned char *)(0xFF210224))
#define Bluetooth_LineControlReg 				((volatile unsigned char *)(0xFF210226))
#define Bluetooth_ModemControlReg 				((volatile unsigned char *)(0xFF210228))
#define Bluetooth_LineStatusReg 				((volatile unsigned char *)(0xFF21022A))
#define Bluetooth_ModemStatusReg 				((volatile unsigned char *)(0xFF21022C))
#define Bluetooth_ScratchReg 					((volatile unsigned char *)(0xFF21022E))
#define Bluetooth_DivisorLatchLSB 				((volatile unsigned char *)(0xFF210220))
#define Bluetooth_DivisorLatchMSB 				((volatile unsigned char *)(0xFF210222))

void Init_BT(void);
int putcharBT (int , volatile unsigned char *,  volatile unsigned char *);
int getcharBT( volatile unsigned char *,  volatile unsigned char *);
int TestForReceivedData(volatile unsigned char *);
void Flush( volatile unsigned char *, volatile unsigned char * );
void BTFactoryReset(void);
void BTOutMessage(char ** Message);

void init_Wifi(void);
int putcharWifi(int c);
void putstringWifi(char*);
int getcharWifi(void);
void getstringWifi(volatile char*);
int WifiTestForReceivedData(void);
void WifiFlush(void);

void Init_RS232(void) {
	// set bit 7 of Line Control Register to 1, to gain access to the baud rate registers
	RS232_LineControlReg = RS232_LineControlReg | 0x80;
	// set Divisor latch (LSB and MSB) with correct value for required baud rate

	int divisor = (int) ((50E6)/(112500 *16));
	RS232_DivisorLatchLSB = divisor & 0xff;
	RS232_DivisorLatchMSB = (divisor >> 8) & 0xff;


	// set bit 7 of Line control register back to 0 and
	RS232_LineControlReg = RS232_LineControlReg & 0x7F;
	// program other bits in that reg for 8 bit data, 1 stop bit, no parity etc
	RS232_LineControlReg = 0x03;
	// Reset the Fifo’s in the FiFo Control Reg by setting bits 1 & 2
	RS232_FifoControlReg = 0x06;
	// Now Clear all bits in the FiFo control registers
	RS232_FifoControlReg = 0x00;
}

int putcharRS232(int c) {
	// wait for Transmitter Holding Register bit (5) of line status register to be '1'
	// indicating we can write to the device
	while((RS232_LineStatusReg & 0x20) != 0x20);
	// write character to Transmitter fifo register
	RS232_TransmitterFifo = c;
	// return the character we printed
	return c;
}

int getcharRS232( void ) {
	// wait for Data Ready bit (0) of line status register to be '1'
	while((RS232_LineStatusReg & 0x01) != 0x01);
	// read new character from ReceiverFiFo register
	int ans = RS232_ReceiverFifo;
	// return new character
	return ans;
}

// the following function polls the UART to determine if any character
// has been received. It doesn't wait for one, or read it, it simply tests
// to see if one is available to read from the FIFO
int RS232TestForReceivedData(void) {
	// if RS232_LineStatusReg bit 0 is set to 1
	//return TRUE, otherwise return FALSE
	if((RS232_LineStatusReg & 0x01) == 0x01)
		return 1;
	return 0;
}

//
// Remove/flush the UART receiver buffer by removing any unread characters
//
void RS232Flush(void) { // read til nothing
	// while bit 0 of Line Status Register == ‘1’
	//    read unwanted char out of fifo receiver buffer
    // return; // no more characters so return
	while((RS232_LineStatusReg & 0x01) == 0x01) {
		int temp = RS232_ReceiverFifo;
	}
	return;
}

// delay function to work with RS323
void delay(long cycles)
{
    long pause;
    clock_t now,then;

    pause = cycles;
    //pause = (long)milliseconds*(CLOCKS_PER_SEC/1000);
    now = then = clock();
    while( (now-then) < pause )
        now = clock();
}

void BTFactoryReset(void)
{
	char c, Message[100] ;
	while(1){
		printf("\r\nEnter Message for Bluetooth Controller:") ;
		gets(Message); // get command string from user keyboard

		printf("The Message is:%s\n", Message);

		int iterator= 0;
		while (Message[iterator] != '\0') {
			putcharBT(Message[iterator], Bluetooth_LineStatusReg , Bluetooth_TransmitterFifo);
			iterator++;
		}

		if(strcmp(Message, "$$$") != 0) {
  		  	  putcharBT('\r', Bluetooth_LineStatusReg , Bluetooth_TransmitterFifo);
  		  	  putcharBT('\n',  Bluetooth_LineStatusReg , Bluetooth_TransmitterFifo );
		}
		// now read back acknowledge string from device and display on console,
		// will timeout after no communication for about 2 seconds
		for(int i = 0; i < 4000000; i ++) {
			if(TestForReceivedData(Bluetooth_LineStatusReg) == 1) {
				c = getcharBT(Bluetooth_LineStatusReg ,   Bluetooth_ReceiverFifo);
				printf("%c", c);
				i=0 ;
			}
		}
	}
}

void BTOutMessage(char ** Message) {
	int iterator=0;
	while(iterator<100 || Message[iterator]!= NULL){
		printf("%c", Message[iterator] );
		iterator ++;
	}
}

void Init_BT(void) {
	// set bit 7 of Line Control Register to 1, to gain access to the baud rate registers
	unsigned char line_control_register= *Bluetooth_LineControlReg;
	line_control_register = line_control_register |  0x80;
	*Bluetooth_LineControlReg= line_control_register;
	// set Divisor latch (LSB and MSB) with correct value for required baud rate
	int divisor = (int) ((50E6)/(38400 *16));
	*Bluetooth_DivisorLatchLSB = divisor & 0xff;
	*Bluetooth_DivisorLatchMSB = (divisor >> 8) & 0xff;

	// set bit 7 of Line control register back to 0 and
	// program other bits in that reg for 8 bit data,
	// 1 stop bit, no parity etc
	*Bluetooth_LineControlReg= 0x03;
	// Reset the Fifo’s in the FiFo Control Reg by setting bits 1 & 2
	*Bluetooth_FifoControlReg = *Bluetooth_FifoControlReg | 0x06;
	// Now Clear all bits in the FiFo control registers
	*Bluetooth_FifoControlReg = *Bluetooth_FifoControlReg ^  0x06;
}

int putcharBT(int c, volatile unsigned char * LineStatusReg ,  volatile unsigned char * TransmitterFifo) {
	// wait for Transmitter Holding Register bit (5) of line status register to be '1'
	// indicating we can write to the device
	while ((*LineStatusReg & 0x20)!= 0x20);
	*TransmitterFifo = (unsigned char)c;
	// write character to Transmitter fifo register
	return c;
	// return the character we printed
}

int getcharBT( volatile unsigned char * LineStatusReg ,  volatile unsigned char *  ReceiverFifo ) {
	while ((*LineStatusReg & 0x01)!= 0x01);
	// wait for Data Ready bit (0) of line status register to be '1'
	// read new character from ReceiverFiFo register
	return (int) *ReceiverFifo;
	// return new character
}

// the following function polls the UART to determine if any character
// has been received. It doesn't wait for one, or read it, it simply tests
// to see if one is available to read from the FIFO
int TestForReceivedData(volatile unsigned char *  LineStatusReg) {
	// if RS232_LineStatusReg bit 0 is set to 1
	if((*LineStatusReg & 0x01)== 0x01){
		return 1;
	}
	else{
		return 0;
	}
}

// main for bluetooth
void GPSReadMessage(char *message){
    int length = 100;
    int i;
    for (i = 0; i < length; i++){
        unsigned char byte =getcharWifi();
        message[i] = byte;
    }
    message[length] = '\0';
}

void ParseGGA(char *message){
    int j = 0;
    while (message[j] != '\n'){
        j++;
    }
    message[j] = '\0';
}
void getGGA(char *message){
    GPSReadMessage(message);
    ParseGGA(message);
}


int main(void) {
	//wifi module...............................................

    init_Wifi();
    // enter the lua mode
    putcharWifi('\r');
    putcharWifi('\n');

    // send a GET request
    putstringWifi("wifi.sta.config('TP-LINK_888','12345687')");
    putstringWifi("wifi.sta.connect()");
    putstringWifi("tmr.delay(1000000)");
    putstringWifi("print(wifi.sta.status())");

    printf("\nprint 5 here\n");

    volatile char c;
    for(int i = 0; i < 4000000; i ++) {
		if(WifiTestForReceivedData() == 1) {
			c = getcharWifi();
			printf("%c", c);
			i=0;
		}
    }

    putstringWifi("print(wifi.sta.getip())");
    putstringWifi("sk=net.createConnection(net.TCP, 0)");
    putstringWifi("sk:on('receive', function(sck, c) print(c) end )");
    putstringWifi("sk:connect(3000,'52.138.39.36')");
    putstringWifi("sk:send('GET /sms\r\nConnection: keep-alive\r\nAccept: */*\r\n\r\n')");

    //volatile char Char = getcharWifi();
    //printf("received %c\n", Char);
    WifiFlush();
	for(int i = 0; i < 4000000; i ++) {
		if(WifiTestForReceivedData() == 1) {
			c = getcharWifi();
			printf("%c", c);
			i=0 ;
		}
	}
    while(1){
    	printf("here it is\n");
    }

void init_Wifi(void) {
	// set bit 7 of Line Control Register to 1, to gain access to the baud rate registers
	unsigned char line_control_register= Wifi_LineControlReg;
	line_control_register = line_control_register |  0x80;
	Wifi_LineControlReg= line_control_register;
	// set Divisor latch (LSB and MSB) with correct value for required baud rate
	int divisor = (int) ((50E6)/(115200 *16));
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
	while ((Wifi_LineStatusReg & 1) == 0){}
	return Wifi_ReceiverFifo;
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





