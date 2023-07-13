#include <xc.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include "pic16f877a.h"

#pragma config FOSC = HS // Yüksek h?zl? osilatör kullan
#pragma config WDTE = OFF // Watchdog Timer'? devre d??? b?rak
#pragma config PWRTE = OFF // Power-up Timer'? devre d??? b?rak
#pragma config BOREN = ON // Brown-out Reset özelli?ini aktif et
#pragma config LVP = OFF // Dü?ük gerilim programlama modunu devre d??? b?rak
#pragma config CPD = OFF // Data EEPROM korumas?n? devre d??? b?rak
#pragma config WRT = OFF // Flash bellek yazmay? devre d??? b?rak
#pragma config CP = OFF // Program bellek korumas?n? devre d??? b?rak

#define _XTAL_FREQ 4000000 // Harici osilatör frekans? (4 MHz)

// Baud rate hesaplama formülü
#define BAUD_RATE 9600

// UART konfigürasyonu
void UART_Init(uint32_t baudrate) {
    TRISCbits.TRISC6 = 0;   // TX pini ç?k?? olarak ayarla
    TRISCbits.TRISC7 = 1;   // RX pini giri? olarak ayarla
    
    SPBRG = (uint16_t)( (_XTAL_FREQ / (baudrate * 16)) - 1 );   // Baudrate hesaplamas?
    TXSTA = 0x24;   // 8-bit veri, asenkron mod, veri gönderimi etkin
    RCSTA = 0x90;   // Seri port etkinle?tirme, 8-bit veri, seri veri alma etkin
}

// Karakter al?m?
char UART_ReadChar() {
    if (RCIF) {      // Veri al?nm?? m? kontrol et
        return RCREG;   // Al?nan veriyi döndür
    } else {
        return 0;       // Veri al?nmam??sa 0 döndür
    }
}

void pwm() {
    TRISC = 0x00; // PORTC'yi ç?k?? olarak ayarla

    CCP1CON = 0b00001111; // CCP1CON register?n? PWM moduna ayarla
    
    T2CON = 0b00000111; // Timer2'yi ayarla: Timer2'yi etkinle?tir, prescaler de?eri 1:4

    TMR2 = 0; // Timer2'yi s?f?rla
    PR2 = 249; // Timer2'nin önölçücü de?erini ayarla (20 ms PWM periyodu için)
}

void main(void) {
    pwm(); 
    UART_Init(BAUD_RATE); // USART'i ba?lat    // Initialize USART with baud rate 9600
    char veri[2];
    char derece[]={'0','1','2','3','4','5','6','7','8','9'};
    int duty, dutydeg, sayi = 0; // PWM görev döngüsü oran?n? ayarla (0-100 aral???nda)
    TRISB = 0;
    PORTB = 0;
    
    // mikrodenetleyicinin görevi sonsuz döngüde uygular
    while(1) {
        
        // Seri porttan iki adet servo motor ad? ve derece bilgisi için karakter al?mlar? için for döngüsü
        for(int i=0;i<2;i++){
        veri[i]=UART_ReadChar(); 
        }
        
        // Servo motorlar? belirleme ve derece bilgisini ay?klama
        for(int i = 0; i < 2; i ++) {
        if (veri[i] == 'a') {
            sayi = veri[i+1] - '0';
            dutydeg = sayi * 20;
            duty = 0.572 * dutydeg + 16;
            
            CCPR1L = (249 * duty) / 180; // PWM yüksek byte'? ayarla (50 Hz için formül)
        }
    
        // di?er servolar için gerekli i?lemleri yapabilirsiniz
    }
        
        
        __delay_ms(100);
        PORTB=0;
        

        
        
        
    }

  
}
