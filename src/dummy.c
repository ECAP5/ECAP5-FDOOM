/*
 * dummy.c
 *
 *  Created on: 16.02.2015
 *      Author: Florian
 */


/*---------------------------------------------------------------------*
 *  include files                                                      *
 *---------------------------------------------------------------------*/

#include "doomtype.h"

/*---------------------------------------------------------------------*
 *  local definitions                                                  *
 *---------------------------------------------------------------------*/

/*---------------------------------------------------------------------*
 *  external declarations                                              *
 *---------------------------------------------------------------------*/

/*---------------------------------------------------------------------*
 *  public data                                                        *
 *---------------------------------------------------------------------*/

boolean net_client_connected = false;

boolean drone = false;

int sfxVolume = 0;
int musicVolume = 0;
int snd_channels = 0;
int netcmds = 0;
int automapactive = 0;

/*---------------------------------------------------------------------*
 *  private data                                                       *
 *---------------------------------------------------------------------*/

/*---------------------------------------------------------------------*
 *  private functions                                                  *
 *---------------------------------------------------------------------*/

/*---------------------------------------------------------------------*
 *  public functions                                                   *
 *---------------------------------------------------------------------*/

void I_Endoom(void) {}
void I_BindSoundVariables(void) {}
void S_UpdateSounds(void) {}
void S_StartMusic(void) {}
void I_InitSound(void) {}
void S_StartSound(void) {}
void S_ChangeMusic(void) {}
void I_InitMusic(void) {}
void S_ResumeSound(void) {}
void S_SetMusicVolume(void) {}
void S_StopSound(void) {}
void S_PauseSound(void) {}
void S_Start(void) {}
void S_Init(void) {}
void S_SetSfxVolume(void) {}

void StatDump(void) {}
void StatCopy(void) {}

void D_ConnectNetGame(void) {}
void D_CheckNetGame(void) {}

void M_BindVariable(void) {}
void M_SetConfigDir(void) {}
void M_SetConfigFilenames(void) {}
void M_LoadDefaults(void) {}
void M_SaveDefaults(void) {}
void M_GetSaveGameDir(void) {}

void AM_Drawer(void) {}
void F_Drawer(void) {}
void AM_Stop(void) {}

void P_SaveGameFile(void) {}

void I_InitJoystick(void) {}

void I_InitInput(void) {}
void I_GetEvent(void) {}

void ST_Drawer(void) {}
void ST_Init(void) {}
void ST_Start(void) {}

#ifndef FEATURE_SOUND

void I_InitTimidityConfig(void)
{
}

#endif

/*---------------------------------------------------------------------*
 *  eof                                                                *
 *---------------------------------------------------------------------*/
