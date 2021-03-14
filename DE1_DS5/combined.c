#include <stdio.h>
#include <time.h>
#include <math.h>

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
#define GPS_ReceiverFifo        				((volatile unsigned char *)(0xFF210210))
#define GPS_TransmitterFifo     				((volatile unsigned char *)(0xFF210210))
#define GPS_InterruptEnableReg  				((volatile unsigned char *)(0xFF210212))
#define GPS_InterruptIdentificationReg 			((volatile unsigned char *)(0xFF210214))
#define GPS_FifoControlReg 						((volatile unsigned char *)(0xFF210214))
#define GPS_LineControlReg 						((volatile unsigned char *)(0xFF210216))
#define GPS_ModemControlReg 					((volatile unsigned char *)(0xFF210218))
#define GPS_LineStatusReg 						((volatile unsigned char *)(0xFF21021A))
#define GPS_ModemStatusReg 						((volatile unsigned char *)(0xFF21021C))
#define GPS_ScratchReg 							((volatile unsigned char *)(0xFF21021E))
#define GPS_DivisorLatchLSB 					((volatile unsigned char *)(0xFF210210))
#define GPS_DivisorLatchMSB 					((volatile unsigned char *)(0xFF210212))
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

void Init_RS232(void) {
	// set bit 7 of Line Control Register to 1, to gain access to the baud rate registers
	RS232_LineControlReg = RS232_LineControlReg | 0x80;
	// set Divisor latch (LSB and MSB) with correct value for required baud rate
	RS232_DivisorLatchLSB = 0x1B;
	RS232_DivisorLatchMSB = 0x00;
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
void delay(long milliseconds)
{
    long pause;
    clock_t now,then;

    pause = 1000;
    //pause = (long)milliseconds*(CLOCKS_PER_SEC/1000);
    now = then = clock();
    while( (now-then) < pause )
        now = clock();
}

void BTFactoryReset(void)
{
	// wait for 1 second between command
	// enter these commands in upper case
	// $$$ enter command mode
	// SF,1 factory reset
	// SN,Device1 set device name to “Device1”
	// SP,1234 set 4 digit pin to “1234”
	// R,1<CR> reboot BT controller
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
	*Bluetooth_DivisorLatchLSB =0x51;
	*Bluetooth_DivisorLatchMSB =0x00;
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

int main(void) {
	Init_BT();
	BTFactoryReset();
	return 0;
}