/*           __        _
 *  ________/ /  ___ _(_)__  ___
 * / __/ __/ _ \/ _ `/ / _ \/ -_)
 * \__/\__/_//_/\_,_/_/_//_/\__/
 * 
 * Copyright (C) Clément Chaine
 * This file is part of ECAP5-DSOC <https://github.com/ecap5/ECAP5-DSOC>
 *
 * ECAP5-DSOC is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * ECAP5-DSOC is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with ECAP5-DSOC.  If not, see <http://www.gnu.org/licenses/>.
 */

OUTPUT_ARCH( "riscv" )
ENTRY(main)
MEMORY
{
  RAM (rwx) : ORIGIN = 0x0, LENGTH = 0x1A000
  /* the flash is not memory mapped, but giving it an address
   * will help determine what needs to be loaded in ram */
  FLASH (r) : ORIGIN = 0x10000000, LENGTH = 0xD00000
}
SECTIONS
{
  .text : { 
    *(.text) 
  } > RAM AT > FLASH

  .rodata : {
    *(.rodata)
  } > RAM AT > FLASH

  .data : {
    *(.data)
    *(.sdata)
  } > RAM AT > FLASH

  .bss : {
    *(.bss)
    *(.sbss)
  } > RAM AT > FLASH

  _stack_top = ORIGIN(RAM) + LENGTH(RAM);
}
