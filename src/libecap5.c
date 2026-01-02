#include <stdio.h>
#include <stddef.h>
#include <string.h>

#define ELF_BASE_ADDRESS 0x300000

#define UART_BASE 0x40000000
#define UART_SR_TXE_MASK (1 << 1)

typedef struct {
  volatile unsigned int sr;
  volatile unsigned int cr;
  volatile unsigned int rxdr;
  volatile unsigned int txdr;
} uart_regs_t;

void set_baudrate(unsigned int acc_incr) {
  uart_regs_t * uart = (uart_regs_t *)UART_BASE;
  uart->cr = (uart->cr & ~(0xFFFF << 16)) | ((acc_incr & 0xFFFF) << 16);
}

void send_char(char * c) {
  uart_regs_t * uart = (uart_regs_t *)UART_BASE;

  // Wait for the uart to be ready
  while(!(uart->sr & UART_SR_TXE_MASK)) {}
  
  uart->txdr = *c;
}

void _exit() {
  printf("(exit error)\n");
  while(1);
}
void _close() {
  // intentionnaly does nothing as there is no file system
}

typedef enum {
  NONE = -1,
  STDIN = 0,
  STDERR = 1,
  WAD = 2,
} opened_file_t;

unsigned int wad_pos;
unsigned int wad_size;
char * wad_data;

extern int _wad_start;
extern int _wad_size;
int _open(const char *pathname, int flags, int mode) {
  if(!strcmp(pathname, "doom1.wad")) {
    wad_pos = 0;
    wad_size = (unsigned int)&_wad_size;
    wad_data = ELF_BASE_ADDRESS + (char*)&_wad_start;
    return WAD;
  } else {
    printf("(open other) %s\n", pathname);
    return NONE;
  }
}

#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2

_off_t _lseek(int fd, _off_t offset, int whence) {
  if(fd == WAD) {
    switch(whence) {
      case SEEK_SET:
        wad_pos = offset;
        break;
      case SEEK_CUR:
        wad_pos = wad_pos + offset;
        break;
      case SEEK_END:
        wad_pos = wad_size + offset;
        break;
    }
//    printf("(seek wad %08x)\n", wad_pos);
  } else {
    printf("(lseek other) %d\n", fd);
  }
}

#include <sys/stat.h>

int _fstat(int fd, struct stat *st) {
  switch(fd) {
    case STDIN:
      st->st_mode = S_IFCHR;
      break;
    case STDERR:
      st->st_mode = S_IFCHR;
      break;
    case WAD:
      st->st_mode = S_IFREG;
      st->st_size = wad_size;
      st->st_blksize = 512;
      break;
    default:
      printf("(fstat other) %d\n", fd);
      return -1;
      break;
  }

  return 0;
}

#define SPI_BASE 0xC0000000
#define SPI_SR_TXE_MASK (1)
#define SPI_FAST_READ 0xB
#define SPI_DUMMY 0x0

typedef struct {
  volatile unsigned int sr;
  volatile unsigned int cr;
  volatile unsigned int rxdr;
  volatile unsigned int txdr;
} spi_regs_t;

char send_spi(char command) {
  spi_regs_t * spi = (spi_regs_t *)SPI_BASE;

  // Wait for the spi to be ready
  while(!(spi->sr & SPI_SR_TXE_MASK)) {}
  
  spi->txdr = command;

  // Wait for the spi to be done
  while(!(spi->sr & SPI_SR_TXE_MASK)) {}

  return spi->rxdr;
}

void get_flash_id(char * id) {
  spi_regs_t * spi = (spi_regs_t *)SPI_BASE;

  // Enable CS
  spi->cr |= 1;

  send_spi(0x9F);
  id[0] = send_spi(0x00);
  id[1] = send_spi(0x00);
  id[2] = send_spi(0x00);

  // Disable CS
  spi->cr &= ~1;
}

size_t copy_flash_to_ram(char * src, char * dst, size_t num) {
  spi_regs_t * spi = (spi_regs_t *)SPI_BASE;

  char address[3] = {
    (((unsigned int)src) >> 16) & 0xFF,
    (((unsigned int)src) >> 8) & 0xFF,
    (unsigned int)src & 0xFF
  };

  // Enable CS
  spi->cr |= 1;

  // Send fast read command
  send_spi(SPI_FAST_READ);
  send_spi(address[0]);
  send_spi(address[1]);
  send_spi(address[2]);
  send_spi(SPI_DUMMY);

  for(size_t i = 0; i < num; i += 1) {
    *dst = send_spi(SPI_DUMMY);  
    dst += 1;
  }

  // Disable CS
  spi->cr &= ~1;

  return num;
}

int _read(int fd, void *buf, size_t nbyte) {
  if(fd == WAD) {
//    printf("(reading %d bytes @ %p)\n", nbyte, wad_data + wad_pos);
    unsigned int num_read_bytes = copy_flash_to_ram(wad_data + wad_pos, buf, nbyte); 
    wad_pos += num_read_bytes;
    return num_read_bytes;
  } else {
    printf("(read other) %d\n", fd);
  }
}

int mkdir(const char *_path, mode_t __mode) {
  printf("(mkdir)\n");
  return -1;
}

extern char _end;
extern char _stack_bottom;
static char * heap_end = &_end;
void * _sbrk(ptrdiff_t incr) {
  char * previous_heap_end = heap_end;
  if((heap_end + incr) < &_stack_bottom) {
    heap_end += incr;
    return previous_heap_end;
  } else {
    printf("Out of memory: requested %d bytes, %d bytes left\n", incr, &_stack_bottom - heap_end);
    return (void*)-1;
  }
}

void _unlink() {
  printf("(unlink)\n");
}
int _isatty(int fd) {
  if(fd == STDIN || fd == STDERR) {
    return 1;
  } else {
    return 0;
  }
}
void _link() {
  printf("(link)\n");
}
void _kill() {
  printf("(kill)\n");
}
void _getpid() {
  printf("(getpid)\n");
}


int _write(int file, char *ptr, int len) {
  for(int i = 0; i < len; i++) {
    send_char(ptr + i); 
  }
}
