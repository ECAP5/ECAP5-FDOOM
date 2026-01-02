#include <stdio.h>

#include "m_argv.h"

#include "doomgeneric.h"

pixel_t* DG_ScreenBuffer = NULL;

void M_FindResponseFile(void);
void D_DoomMain (void);


void doomgeneric_Create(int argc, char **argv)
{
	// save arguments
  myargc = argc;
  myargv = argv;

  // Allocate the screen buffer
	DG_ScreenBuffer = malloc(DOOMGENERIC_RESX * DOOMGENERIC_RESY);
  for(size_t i = 0; i < DOOMGENERIC_RESX * DOOMGENERIC_RESY; i++) {
    DG_ScreenBuffer[i] = 0x0;
  }

	DG_Init();

	D_DoomMain();
}

