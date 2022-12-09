### This is using python script to try to automate procedures for recovery of module from uboot commands.
- for recovery process, `u-boot`have to be working;
- GUI is designed basing on `pysimplegui` module (https://pysimplegui.readthedocs.io/en/latest/);
- some custom files are needed (project specific);
- for factory test, you have to put commands to be run into a text file named "cmdlist.txt", same as the bin directory.
- release is made for windows only, using autopytoexe module.


note: `to use recovery, you have to get a swuimage and put it onto USB drive, insert it to board where uboot has access.`
