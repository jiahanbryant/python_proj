### This is to add a simple GUI to uuu tool, for simplicity of use
`uuu` Universal Update Utility, made by NXP(Freescale), see more here
https://github.com/NXPmicro/mfgtools
- The tool loads uboot and fit image onto ram and CPU will run from there, meaning this will not affect the content on flash;
- Only when the fit image is booted you can make change on flash, use for example:
    - `flash boot` command to flash u-boot and fit image, these files are embeded in the fit image, now it's taken care by `recover` button. 
    - `verify` command to check basic information.
    - `help` command to check supported commands.
- commands are issued via SoC's debug uart interface.
