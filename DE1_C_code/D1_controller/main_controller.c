#include <stdio.h>
#include <time.h>
#include <math.h>

// address of hardware acceleration
#define simpleBox (volatile int *) 0xFF202060	//whiteTwo 100

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

// Remove/flush the UART receiver buffer by removing any unread characters
void RS232Flush(void) { // read til nothing
	// while bit 0 of Line Status Register == ‘1’
	// read unwanted char out of fifo receiver buffer
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

void Init_BT(void) {
	// set bit 7 of Line Control Register to 1, to gain access to the baud rate registers
	*Bluetooth_LineControlReg= *Bluetooth_LineControlReg | 0x80;
	// set Divisor latch (LSB and MSB) with correct value for required baud rate
	int divisor = (int) ((50E6)/(112500 *16));
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

int getHexDigit(int x, int n) {
    return (x >> (n << 2)) & 0xff;
}

// main function for sonar sensor and hardware acceleration module
int main(void) {
	Init_BT();
	Init_RS232();

	while(1){
		int logout = 0;
		int counter = 0;
		int width = 160;
		int height = 90;

		// display the Sonar sensor on the HEX display of the DE1
		while(1){
			while(RS232TestForReceivedData() != 1);
			int distance = getcharRS232();
			printf("sonar received:%d\n", distance);
			unsigned char value = distance;
			unsigned char first;
			unsigned char second;
			unsigned char third;
			first = value%10;
			value = value/10;
			second = value%10;
			value = value/10;
			third = value%10;
			*HEX0_1 = first;
			*HEX2_3 = second;
			*HEX4_5 = third;
			if(distance < 15){
				*LEDS = 1023;
			}else{
				*LEDS = 0;
			}

			// logout logic
			if(logout == 5){
				break;
			}else if(distance == 0){
				logout++;
			}
		}

		printf("done sonar :)))\n");

		// reset signal to reset hardware acceleration
		*simpleBox = 0x1869F;
		printf("value is now %x, %d\n", *simpleBox, *simpleBox);

		// receive image and send it to hardware acceleration module
		while(counter < 3*height*width){
			if(RS232TestForReceivedData() == 1) {
				*simpleBox = 2*getcharRS232()*0x1000000;
				//printf("%d\n", counter);
				counter++;
			}
		}
		printf("value is now %x, %d\n", *simpleBox, *simpleBox);

		printf("done image cropping :)))\n");

		printf("0 is now %x, %d\n", getHexDigit(*simpleBox,0), getHexDigit(*simpleBox,0));
		printf("2 is now %x, %d\n", getHexDigit(*simpleBox,2), getHexDigit(*simpleBox,2));
		printf("2 is now %x, %d\n", getHexDigit(*simpleBox,4), getHexDigit(*simpleBox,4));
		printf("2 is now %x, %d\n", getHexDigit(*simpleBox,6), getHexDigit(*simpleBox,6));

		int boundingBoxCount = 0;
		int next = 1;
		// send data of the bounding box to rpi
		while(1){
			printf("here");
			if(boundingBoxCount == 8){
				break;
			}
			if(next == 1){
				printf("%d\n", boundingBoxCount);
				putcharBT(getHexDigit(*simpleBox,boundingBoxCount), Bluetooth_LineStatusReg , Bluetooth_TransmitterFifo);
				next = 0;
			}
			if(TestForReceivedData(Bluetooth_LineStatusReg) == 1) {
				boundingBoxCount = boundingBoxCount + 2;
				next = 1;
			}
		}
	}
}
