//#include <stdio.h>
//#include <time.h>
//
//// C:/intelFPGA_lite/18.1/quartus/bin64/quartus_hps --cable="DE-SoC [USB-1]" -o GDBSERVER --gdbport0=3335 -preloader=C:/intelFPGA_lite/18.1/University_Program/Monitor_Program/arm_tools/u-boot-spl.de1-soc.srec -preloaderaddr=0xffff13a0
//#define RS232_ReceiverFifo         				(*(volatile unsigned char *)(0xFF210200))
//#define RS232_TransmitterFifo      				(*(volatile unsigned char *)(0xFF210200))
//#define RS232_InterruptEnableReg   				(*(volatile unsigned char *)(0xFF210202))
//#define RS232_InterruptIdentificationReg        (*(volatile unsigned char *)(0xFF210204))
//#define RS232_FifoControlReg                    (*(volatile unsigned char *)(0xFF210204))
//#define RS232_LineControlReg                    (*(volatile unsigned char *)(0xFF210206))
//#define RS232_ModemControlReg                   (*(volatile unsigned char *)(0xFF210208))
//#define RS232_LineStatusReg                     (*(volatile unsigned char *)(0xFF21020A))
//#define RS232_ModemStatusReg                    (*(volatile unsigned char *)(0xFF21020C))
//#define RS232_ScratchReg                        (*(volatile unsigned char *)(0xFF21020E))
//
//#define RS232_DivisorLatchLSB                   (*(volatile unsigned char *)(0xFF210200))
//#define RS232_DivisorLatchMSB                   (*(volatile unsigned char *)(0xFF210202))
////...............................................................................................
//
//
////#define Bluetooth_ReceiverFifo        ((volatile unsigned char *)(0xFF210220))
////#define Bluetooth_TransmitterFifo     ((volatile unsigned char *)(0xFF210220))
////#define Bluetooth_InterruptEnableReg  ((volatile unsigned char *)(0xFF210222))
////#define Bluetooth_InterruptIdentificationReg ((volatile unsigned char *)(0xFF210224))
////#define Bluetooth_FifoControlReg ((volatile unsigned char *)(0xFF210224))
////#define Bluetooth_LineControlReg ((volatile unsigned char *)(0xFF210226))
////#define Bluetooth_ModemControlReg ((volatile unsigned char *)(0xFF210228))
////#define Bluetooth_LineStatusReg ((volatile unsigned char *)(0xFF21022A))
////#define Bluetooth_ModemStatusReg ((volatile unsigned char *)(0xFF21022C))
////#define Bluetooth_ScratchReg ((volatile unsigned char *)(0xFF21022E))
////#define Bluetooth_DivisorLatchLSB ((volatile unsigned char *)(0xFF210220))
////#define Bluetooth_DivisorLatchMSB ((volatile unsigned char *)(0xFF210222))
////#define TRUE 1
////#define FALSE 0
//
////void Init_BT(void);
////int putchar_uart (int  , volatile unsigned char *  ,  volatile unsigned char * );
////int getchar_uart( volatile unsigned char *  ,  volatile unsigned char *   );
////int TestForReceivedData(volatile unsigned char *  );
////void Flush( volatile unsigned char *   , volatile unsigned char *  );
////void BTFactoryReset(void);
////void BTOutMessage(char ** Message);
//
////.................................................................................
//
//#define Bluetooth_Offset                        (volatile unsigned char *)(0x00000020)
//#define Bluetooth_ReceiverFifo                  (*(volatile unsigned char *)((int)Bluetooth_Offset + (int)&RS232_ReceiverFifo))
//#define Bluetooth_TransmitterFifo               (*(volatile unsigned char *)((int)Bluetooth_Offset + (int)&RS232_TransmitterFifo))
//#define Bluetooth_InterruptEnableReg            (*(volatile unsigned char *)((int)Bluetooth_Offset + (int)&RS232_InterruptEnableReg))
//#define Bluetooth_InterruptIdentificationReg    (*(volatile unsigned char *)((int)Bluetooth_Offset + (int)&RS232_InterruptIdentificationReg))
//#define Bluetooth_FifoControlReg                (*(volatile unsigned char *)((int)Bluetooth_Offset + (int)&RS232_FifoControlReg))
//#define Bluetooth_LineControlReg                (*(volatile unsigned char *)((int)Bluetooth_Offset + (int)&RS232_LineControlReg))
//#define Bluetooth_ModemControlReg               (*(volatile unsigned char *)((int)Bluetooth_Offset + (int)&RS232_ModemControlReg))
//#define Bluetooth_LineStatusReg                 (*(volatile unsigned char *)((int)Bluetooth_Offset + (int)&RS232_LineStatusReg))
//#define Bluetooth_ModemStatusReg                (*(volatile unsigned char *)((int)Bluetooth_Offset + (int)&RS232_ModemStatusReg))
//#define Bluetooth_ScratchReg                    (*(volatile unsigned char *)((int)Bluetooth_Offset + (int)&RS232_ScratchReg))
//#define Bluetooth_DivisorLatchLSB               (*(volatile unsigned char *)((int)Bluetooth_Offset + (int)&RS232_DivisorLatchLSB))
//#define Bluetooth_DivisorLatchMSB               (*(volatile unsigned char *)((int)Bluetooth_Offset + (int)&RS232_DivisorLatchMSB))
//
//#define WiFi_Offset                        (volatile unsigned char *)(0x00000010)
//#define WiFi_ReceiverFifo                  (*(volatile unsigned char *)((int)WiFi_Offset + (int)&RS232_ReceiverFifo))
//#define WiFi_TransmitterFifo               (*(volatile unsigned char *)((int)WiFi_Offset + (int)&RS232_TransmitterFifo))
//#define WiFi_InterruptEnableReg            (*(volatile unsigned char *)((int)WiFi_Offset + (int)&RS232_InterruptEnableReg))
//#define WiFi_InterruptIdentificationReg    (*(volatile unsigned char *)((int)WiFi_Offset + (int)&RS232_InterruptIdentificationReg))
//#define WiFi_FifoControlReg                (*(volatile unsigned char *)((int)WiFi_Offset + (int)&RS232_FifoControlReg))
//#define WiFi_LineControlReg                (*(volatile unsigned char *)((int)WiFi_Offset + (int)&RS232_LineControlReg))
//#define WiFi_ModemControlReg               (*(volatile unsigned char *)((int)WiFi_Offset + (int)&RS232_ModemControlReg))
//#define WiFi_LineStatusReg                 (*(volatile unsigned char *)((int)WiFi_Offset + (int)&RS232_LineStatusReg))
//#define WiFi_ModemStatusReg                (*(volatile unsigned char *)((int)WiFi_Offset + (int)&RS232_ModemStatusReg))
//#define WiFi_ScratchReg                    (*(volatile unsigned char *)((int)WiFi_Offset + (int)&RS232_ScratchReg))
//#define WiFi_DivisorLatchLSB               (*(volatile unsigned char *)((int)WiFi_Offset + (int)&RS232_DivisorLatchLSB))
//#define WiFi_DivisorLatchMSB               (*(volatile unsigned char *)((int)WiFi_Offset + (int)&RS232_DivisorLatchMSB))
//
//
//void delay(long milliseconds)
//{
//    long pause;
//    clock_t now,then;
//
//    pause = 200;
//    //pause = (long)milliseconds*(CLOCKS_PER_SEC/1000);
//    now = then = clock();
//    while( (now-then) < pause )
//        now = clock();
//}
//
//void Init_RS232(void) {
//	// set bit 7 of Line Control Register to 1, to gain access to the baud rate registers
//	RS232_LineControlReg = RS232_LineControlReg | 0x80;
//	// set Divisor latch (LSB and MSB) with correct value for required baud rate
//
//	int divisor = (int) ((50E6)/(112500 *16));
//	RS232_DivisorLatchLSB = divisor & 0xff;
//	RS232_DivisorLatchMSB = (divisor >> 8) & 0xff;
//
//
//	// set bit 7 of Line control register back to 0 and
//	RS232_LineControlReg = RS232_LineControlReg & 0x7F;
//	// program other bits in that reg for 8 bit data, 1 stop bit, no parity etc
//	RS232_LineControlReg = 0x03;
//	// Reset the Fifo’s in the FiFo Control Reg by setting bits 1 & 2
//	RS232_FifoControlReg = 0x06;
//	// Now Clear all bits in the FiFo control registers
//	RS232_FifoControlReg = 0x0;
////	RS232_LineControlReg = 0x80;
////
////	RS232_DivisorLatchLSB = 0x1;
////	RS232_DivisorLatchMSB = 0x9;
////
////	RS232_LineControlReg = 0x02;
////
////	RS232_FifoControlReg = 0x06;
////	RS232_FifoControlReg = 0x00;
//}
//
//int putcharRS232(int c) {
//	// wait for Transmitter Holding Register bit (5) of line status register to be '1'
//	// indicating we can write to the device
//	while((RS232_LineStatusReg & 0x20) != 0x20);
//	// write character to Transmitter fifo register
//	RS232_TransmitterFifo = c;
//	// return the character we printed
//	return c;
//}
//
//int getcharRS232( void ) {
//	// wait for Data Ready bit (0) of line status register to be '1'
//	while((RS232_LineStatusReg & 0x01) != 0x01);
//	// read new character from ReceiverFiFo register
//	int ans = RS232_ReceiverFifo;
//	// return new character
//	return ans;
//}
//
//// the following function polls the UART to determine if any character
//// has been received. It doesn't wait for one, or read it, it simply tests
//// to see if one is available to read from the FIFO
//
//int RS232TestForReceivedData(void) {
//	// if RS232_LineStatusReg bit 0 is set to 1
//	//return TRUE, otherwise return FALSE
//	if((RS232_LineStatusReg & 0x01) == 0x01)
//		return 1;
//	return 0;
//}
//
////
//// Remove/flush the UART receiver buffer by removing any unread characters
////
//
//void RS232Flush(void) { // read til nothing
//	// while bit 0 of Line Status Register == ‘1’
//	//    read unwanted char out of fifo receiver buffer
//    // return; // no more characters so return
//	while((RS232_LineStatusReg & 0x01) == 0x01) {
//		int temp = RS232_ReceiverFifo;
//	}
//	return;
//}
//
//
//
//
//
//
//
//
//
//
////int main(void) {
////
////
////	int iterator, i;
////	Init_BT();
////	BTFactoryReset();
////
////
//////	Init_RS232();
////
////
//////	char Message[100] ;
//////	while(1){
//////		printf("\r\nEnter Message for rs232 Controller:") ;
//////		gets(Message);
//////		printf("send rs232 message is:%s\n", Message);
//////
//////		int iterator= 0;
//////		while (Message[iterator] != '\0') {
//////			putcharRS232(Message[iterator]);
//////			iterator++;
//////		}
//////	}
////
//////	int i;
//////	for(i = 0; i < 255; i ++) {
//////		printf("send rs232 num is:%d\n", i);
//////		putcharRS232(i);
//////		//delay(10);
//////	}
////
////
//////	int i;
//////	for(i = 0; i < 255; i ++) {
//////		printf("send rs232 num is:%d\n", i);
//////		putcharRS232(i);
//////
//////		while(RS232TestForReceivedData() != 1 && getcharRS232() != 57){
//////			putcharRS232(i);
//////			int answer = getcharRS232();
//////			printf("received: %d\n", answer);;
//////		}
//////	}
////
////
////
//////RS232TestForReceivedData() != 1
////
//////	if(num != ans)
//////		printf("Error, the words are not the same.");
//////	else
//////		printf("Success, words are the same.");
//////	RS232Flush();
////	return 0;
////}
////
////
////
////
////
////
////
////void BTFactoryReset(void)
////{
////// wait for 1 second between command
////// enter these commands in upper case
////// $$$ enter command mode
////// SF,1 factory reset
////// SN,Device1 set device name to “Device1”
////// SP,1234 set 4 digit pin to “1234”
////// R,1<CR> reboot BT controller
////	char c, Message[100] ;
////	int i;
////	while(1){
////		printf("\r\nEnter Message for Bluetooth Controller:") ;
////		gets(Message); // get command string from user keyboard
//// //BTOutMessage(&Message) ; // write string to BT device
////		printf("THE Message IS:%s\n", Message);
////
////		int iterator= 0;
////		while (Message[iterator] != '\0') {
////			putchar_uart(Message[iterator], Bluetooth_LineStatusReg , Bluetooth_TransmitterFifo) ;
////			iterator++;
////		}
//// // if the command string was NOT "$$$" send \r\n
////		if(strcmp(Message, "$$$") != 0) { // $$$ puts BT module into command mode
////  		  	  putchar_uart('\r', Bluetooth_LineStatusReg , Bluetooth_TransmitterFifo) ;
////  		  	  putchar_uart('\n',  Bluetooth_LineStatusReg , Bluetooth_TransmitterFifo ) ;
////		}
//// // now read back acknowledge string from device and display on console,
//// // will timeout after no communication for about 2 seconds
////		for(i = 0; i < 2000000000; i ++) {
////			if(TestForReceivedData(Bluetooth_LineStatusReg) == 1) {
////				c = getchar_uart(Bluetooth_LineStatusReg ,   Bluetooth_ReceiverFifo) ;
////				printf("%c", c);
////				i=0 ; // reset timer if we got something back
////			}
////		}
////	}
////}
////
////void BTOutMessage(char ** Message){
////int iterator=0;
//////while(iterator<100 || Message[iterator]!= NULL){
//////	putchar_uart(*Message[iterator],Bluetooth_LineStatusReg , Bluetooth_TransmitterFifo);
//////	iterator++;
//////}
////while(iterator<100 || Message[iterator]!= NULL){
//////	putchar_uart(*Message[iterator],Bluetooth_LineStatusReg , Bluetooth_TransmitterFifo);
//////	iterator++;
////printf("%c", Message[iterator] );
////iterator ++;
////}
////
////}
////
////
////void Init_BT(void)
////{
////
////// set bit 7 of Line Control Register to 1, to gain access to the baud rate registers
////unsigned char line_control_register;
////line_control_register= *Bluetooth_LineControlReg;
////line_control_register = line_control_register |  0x80;
////*Bluetooth_LineControlReg= line_control_register;
//// // set Divisor latch (LSB and MSB) with correct value for required baud rate
////// example 0x0145
//// *Bluetooth_DivisorLatchLSB =0x51;
//// *Bluetooth_DivisorLatchMSB =0x00;
//// // set bit 7 of Line control register back to 0 and
//// // program other bits in that reg for 8 bit data,
//// // 1 stop bit, no parity etc
//// //0000 0011
//// *Bluetooth_LineControlReg= 0x03;
//// // Reset the Fifo’s in the FiFo Control Reg by setting bits 1 & 2
////*Bluetooth_FifoControlReg = *Bluetooth_FifoControlReg | 0x06;
//// // Now Clear all bits in the FiFo control registers
////*Bluetooth_FifoControlReg = *Bluetooth_FifoControlReg ^  0x06;
////}
////
////
////
////int putchar_uart(int c, volatile unsigned char *  LineStatusReg ,  volatile unsigned char *  TransmitterFifo)
////{
//// // wait for Transmitter Holding Register bit (5) of line status register to be '1'
//// // indicating we can write to the device
//// while ( (*LineStatusReg & 0x20)!= 0x20){
////;
//// }
//// *TransmitterFifo = (unsigned char)c;
////// write character to Transmitter fifo register
////return c;
////// return the character we printed
////
////}
////int getchar_uart( volatile unsigned char *  LineStatusReg ,  volatile unsigned char *  ReceiverFifo )
////{
////
////  while ( (*LineStatusReg & 0x01)!= 0x01){
////
//// ;
////  }
//// // wait for Data Ready bit (0) of line status register to be '1'
//// // read new character from ReceiverFiFo register
//// return (int) *ReceiverFifo;
//// // return new character
////}
////// the following function polls the UART to determine if any character
////// has been received. It doesn't wait for one, or read it, it simply tests
////// to see if one is available to read from the FIFO
////int TestForReceivedData(volatile unsigned char *  LineStatusReg)
////{
//// // if RS232_LineStatusReg bit 0 is set to 1
//// if((*LineStatusReg & 0x01)== 0x01)
//// return TRUE;
//// else
//// return FALSE;
//// //return TRUE, otherwise return FALSE
////}
//
//
//
//
////..................................................
//
//void BTOutMessage (char * Message){
//    int i;
//    for(i = 0; Message[i] != '\0'; i++) { putcharBT(Message[i]);}
//}
//void BT_Flush (void)
//{
//    volatile int temp = 0;
//    while(Bluetooth_LineStatusReg & 1) {temp = Bluetooth_ReceiverFifo;}
//    return;
//}
//
////#include <io.h>
//void BTFactoryReset (void)
//{
//    // wait for 1 second between command
//    // enter these commands in upper case
//    // $$$ enter command mode
//    // SF,1 factory reset
//    // SN,Device1 set device name to “Device1”
//    // SP,1234 set 4 digit pin to “1234”
//    // R,1<CR> reboot BT controller
//
//    char c, Message[100] ;
//    int i;
//    char temp[20];
//
//    while(1) {
//
//        printf("\r\nEnter Message for Bluetooth Controller: ") ;
//        gets(Message); // get command string from user keyboard
//        gets(temp);
//        BTOutMessage(Message) ; // write string to BT device
//
//        // if the command string was NOT "$$$" send \r\n
//        if(strcmp(Message, "$$$") != 0) { // $$$ puts BT module into command mode
//            putcharBT('\r') ;
//            putcharBT('\n') ;
//        }
//
//        // now read back acknowledge string from device and display on console,
//        // will timeout after no communication for about 2 seconds
//        for(i = 0; i < 2000000; i ++) {
//            if(testBT() == 1) {
//                c = getcharBT();
//                putchar(c);
//            }
//        }
//    }
//}
//
//int testBT (void)
//{
//    if((Bluetooth_LineStatusReg & 1)){
//        return 1;
//    }
//    return 0;
//}
//
//void Init_BT (void)
//{
//    Bluetooth_LineControlReg = 0x80;
//    int divisor = (int) ((50E6)/(38400 *16));
//    Bluetooth_DivisorLatchLSB = divisor & 0xff;
//    Bluetooth_DivisorLatchMSB = (divisor >> 8) & 0xff;
//
//    Bluetooth_LineControlReg = 0x33;
//    Bluetooth_FifoControlReg = 0x6;
//    Bluetooth_FifoControlReg = 0;
//}
//
//int putcharBT (int  c)
//{
//    while( ((Bluetooth_LineStatusReg >> 5) & 1) == 0){}
//    Bluetooth_TransmitterFifo = c;
//    return c;
//}
//
//int getcharBT (void)
//{
//    // wait for Data Ready bit (0) of line status register to be '1'
//    while ( (Bluetooth_LineStatusReg & 1) == 0){}
//
//    // read new character from ReceiverFiFo register
//    return Bluetooth_ReceiverFifo;
//}
//
//// the following function polls the UART to determine if any character
//// has been received. It doesn't wait for one, or read it, it simply tests
//// to see if one is available to read from the FIFO
//int BT_TestForReceivedData (void)
//{
//    // if Bluetooth LineStatusReg bit 0 is set to 1
//    return (Bluetooth_LineStatusReg & 1);
//}
////...........................................................................................
//
//void WFOutMessage (char * Message){
//    int i;
//    for(i = 0; Message[i] != '\0'; i++) { putcharWF(Message[i]);}
//}
//void WF_Flush (void)
//{
//    volatile int temp = 0;
//    while(WiFi_LineStatusReg & 1) {temp = WiFi_ReceiverFifo;}
//    return;
//}
//
////#include <io.h>
//void WFFactoryReset (void)
//{
//    // wait for 1 second between command
//    // enter these commands in upper case
//    // $$$ enter command mode
//    // SF,1 factory reset
//    // SN,Device1 set device name to “Device1”
//    // SP,1234 set 4 digit pin to “1234”
//    // R,1<CR> reboot BT controller
//
//    char c, Message[100] ;
//    int i;
//    char temp[20];
//
//    while(1) {
//
//        printf("\r\nEnter Message for WiFi Controller: ") ;
//        gets(Message); // get command string from user keyboard
//        gets(temp);
//        printf("\r\nhere wifi send");
//        WFOutMessage(Message) ; // write string to BT device
//
//        // if the command string was NOT "$$$" send \r\n
//        if(strcmp(Message, "$$$") != 0) { // $$$ puts BT module into command mode
//            putcharWF('\r') ;
//            putcharWF('\n') ;
//        }
//
//        // now read back acknowledge string from device and display on console,
//        // will timeout after no communication for about 2 seconds
//        for(i = 0; i < 2000000; i ++) {
//            if(testWF() == 1) {
//                c = getcharWF();
//                putchar(c);
//            }
//        }
//    }
//}
//
//int testWF (void)
//{
//    if((WiFi_LineStatusReg & 1)){
//        return 1;
//    }
//    return 0;
//}
//
//void Init_WF (void)
//{
//	WiFi_LineControlReg = 0x80;
//    int divisor = (int) ((50E6)/(115200 *16));
//    WiFi_DivisorLatchLSB = divisor & 0xff;
//    WiFi_DivisorLatchMSB = (divisor >> 8) & 0xff;
//
//    WiFi_LineControlReg = 0x33;
//    WiFi_FifoControlReg = 0x6;
//    WiFi_FifoControlReg = 0;
//}
//
//int putcharWF (int  c)
//{
//	while((WiFi_LineStatusReg & 0x20) != 0x20){
//		printf("waiting\r\n");
//	};
//    //while( ((WiFi_LineStatusReg >> 5) & 1) == 0){}
//    WiFi_TransmitterFifo = c;
//    return c;
//}
//
//int getcharWF (void)
//{
//    // wait for Data Ready bit (0) of line status register to be '1'
//    while ( (WiFi_LineStatusReg & 1) == 0){}
//
//    // read new character from ReceiverFiFo register
//    return WiFi_ReceiverFifo;
//}
//
//// the following function polls the UART to determine if any character
//// has been received. It doesn't wait for one, or read it, it simply tests
//// to see if one is available to read from the FIFO
//int WF_TestForReceivedData (void)
//{
//    // if WiFi LineStatusReg bit 0 is set to 1
//    return (WiFi_LineStatusReg & 1);
//}
//
//void main(){
//
////	Init_RS232();
////
////	int i;
////	for(i = 0; i < 255; i ++) {
////		printf("send rs232 num is:%d\n", i);
////		putcharRS232(i);
////	}
////
////
////
////    Init_BT();
////    BTFactoryReset();
//
//    Init_WF();
//    WFFactoryReset();
//}
//
//
//
//........................................................................

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
int main(void) {
	Init_BT();
	Init_RS232();
//	BTFactoryReset();
	while(1){
			int usernameCounter = 0;
			int username[100];
			// waiting for sign in from the user


			while(1){
				if(TestForReceivedData(Bluetooth_LineStatusReg) == 1) {
					int c = getcharBT(Bluetooth_LineStatusReg , Bluetooth_ReceiverFifo);
					if(c != 13 && c != 10){
						printf("received %d from the Bluetooth \n", c);
						username[usernameCounter] = c;

						if(c == 50 || c == 49){ //customer1 and customer2
							break;
						}
						usernameCounter ++;
					}

				}
			}

			// send username to Raspberry Pi
			for(int i = 0; i <= usernameCounter; i++){
				printf("send rs232 to RPI:%d\n", username[i]);
				putcharRS232(username[i]);
			}

	}


//	int logout = 0;
//	// Sonar sensor
//	while(1){
//		while(RS232TestForReceivedData() != 1);
//		int distance = getcharRS232();
//		printf("sonar received:%d\n", distance);
//		unsigned char value = distance;
//		unsigned char first;
//		unsigned char second;
//		unsigned char third;
//		first = value%10;
//		value = value/10;
//		second = value%10;
//		value = value/10;
//		third = value%10;
//		*HEX0_1 = first;
//		*HEX2_3 = second;
//		*HEX4_5 = third;
//		if(distance < 20){
//			*LEDS = 1023;
//		}else{
//			*LEDS =0;
//		}
//
//		// logout logic
//		if(logout == 5){
//			break;
//		}else if(distance == 200){
//			logout++;
//		}
//	}
}

//for(int i = 0; i < 255; i++){
//	delay(100);
//	printf("trasmit %d to the Bluetooth \n", i);
//	putcharBT(i, Bluetooth_LineStatusReg , Bluetooth_TransmitterFifo);
//}
//
////main for RS232 read
//int main(void) {
//	Init_RS232();
//	while(1){
//		while(RS232TestForReceivedData() != 1);
//		int distance = getcharRS232();
//		printf("received:%d\n", distance);
//		unsigned char value = distance;
//		unsigned char first;
//		unsigned char second;
//		unsigned char third;
//		first = value%10;
//		value = value/10;
//		second = value%10;
//		value = value/10;
//		third = value%10;
//		*HEX0_1 = first;
//		*HEX2_3 = second;
//		*HEX4_5 = third;
//		if(distance < 20){
//			*LEDS = 1023;
//		}
//		else{
//			*LEDS =0;
//		}
//	}
//}

// main for RS232 write
//void main(){
//	Init_RS232();
//	int i;
//	for(i = 0; i < 255; i ++) {
//		printf("send rs232 num is:%d\n", i);
//		putcharRS232(i);
//	}
//}







