#include "doomgeneric.h"

void DG_Init() {

}

void DG_DrawFrame() {
  printf("DRAW\n");
}

#define TIMER_BASE 0x80000000

typedef struct {
  volatile unsigned int timebase_low;
  volatile unsigned int timebase_high;
} timer_regs_t;

uint32_t DG_GetTicksMs() {
  timer_regs_t * timer = (timer_regs_t *)TIMER_BASE;

  return timer->timebase_low;
}

void DG_SleepMs(uint32_t ms) {
  unsigned int start_time = DG_GetTicksMs();
  while(DG_GetTicksMs() - start_time < ms) {}
  return;
}

int DG_GetKey(int* pressed, unsigned char* doomKey) {
  return 0;
}

void DG_SetWindowTitle(const char * title) {
  return;
}

extern int _wad_start;
void main(void) {
  int argc = 0;
  char * argv[] = {};
  doomgeneric_Create(argc, argv);

  while(1) {
    doomgeneric_Tick();
  }
}
