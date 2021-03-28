#include <stdio.h>
#include <time.h>
#define simpleBox (volatile int *) 0xFF202070

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

int main()
{
	int value = 1;

	// reset signal
	*simpleBox = 0x1869F;

	printf("value is now %x, %d\n", *simpleBox, *simpleBox);

	for(int i = 0; i < 3*100*100; i++){
		if(i == 22275 || i == 11880){
			*simpleBox = 1*0x1000000; // write the value to component
		} else{
			*simpleBox = 255*0x1000000;
		}
		//printf("value is now %x\n", *simpleBox);
	}
	printf("value is now %x, %d\n", *simpleBox, *simpleBox);

    // reset signal
	*simpleBox = 0x1869F;

	for(int i = 0; i < 3*100*100; i++){
		*simpleBox = 255*0x1000000;
		//printf("value is now %x\n", *simpleBox);
	}
	printf("value is now %x, %d\n", *simpleBox, *simpleBox);

    // reset signal
	*simpleBox = 0x1869F;

	for(int i = 0; i < 3*100*100; i++){
		*simpleBox = 1*0x1000000;
		//printf("value is now %x\n", *simpleBox);
	}
	printf("value is now %x, %d\n", *simpleBox, *simpleBox);
}
