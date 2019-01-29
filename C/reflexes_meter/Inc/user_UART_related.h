#include <stdint.h>

#define UART1_TXBUFFER_SIZE 5
#define UART1_RXBUFFER_SIZE 2

/* Possible rx commands */
typedef enum {
	INVALID,
	TURN_LED_ON,
	TURN_LED_OFF
} UART_RxCmdTypeDef;

/* Exported functions */
UART_RxCmdTypeDef UART_ParseRxCommand(uint8_t *UART_rxBuffer);
