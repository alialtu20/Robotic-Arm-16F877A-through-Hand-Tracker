#include <xc.h>
#include <stdio.h>
#include <stdint.h>
#include "pic16f877a.h"

#pragma config FOSC = HS 
#pragma config WDTE = OFF 
#pragma config PWRTE = OFF 
#pragma config BOREN = ON 
#pragma config LVP = OFF 
#pragma config CPD = OFF 
#pragma config WRT = OFF 
#pragma config CP = OFF 

#define _XTAL_FREQ 4000000 
#define BAUD_RATE 9600

void UART_Init(uint32_t baudrate) {
    TRISCbits.TRISC6 = 0;
    TRISCbits.TRISC7 = 1;
    
    SPBRG = (uint16_t)( (_XTAL_FREQ / (baudrate * 16)) - 1 );
    TXSTA = 0x24;
    RCSTA = 0x90;
}

char UART_ReadChar() {
    if(RCIF) {
        return RCREG; 
    } 
    else {
        return 0;
    }
}

void PWM_Init() {
    TRISC = 0x00;
    CCP1CON = 0b00001111;
    T2CON = 0b00000111;
    TMR2 = 0;
    PR2 = 249;
}

void main(void) {
    char veri[2];
    char derece[]={'0','1','2','3','4','5','6','7','8','9'};
    uint16_t duty, dutydeg, sayi = 0;
    TRISB = 0;
    PORTB = 0;

    PWM_Init(); 
    UART_Init(BAUD_RATE);
    
    while(1) {
        
        for(uint8_t i=0;i<2;i++) {
        veri[i]=UART_ReadChar(); 
        }
        
        for(uint8_t i = 0; i < 2; i ++) {
            if (veri[i] == 'a') {
                sayi = veri[i+1] - '0';
                dutydeg = sayi * 20;
                duty = 0.572 * dutydeg + 16;
            
                CCPR1L = (249 * duty) / 180;
            }
         }  
         __delay_ms(100);
         PORTB=0;
    }
}
