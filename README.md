![DS Nitro Builder Banner](https://github.com/zigaudrey/DS-nitro-file-builder/assets/129554573/b7197262-f7bb-4bb1-ab26-fa289d74a30e)
# DS Nitro files Builder
A Python-Script that convert a picture into Nitro files for Nintendo DS Rom Hacking

## Steps
1. If you don't have PIL, **open the console and install with PIP**
1. Launch **the script in the console so PIL will works**
1. Choose a picture you want to convert. It has to be **under or equal to 256x192 and both dimensions a divisible of 8**
1. Choose the color depth. It is **best to match the depth from the original picture and use a drawing software to check how many colors it has**
1. Choose the X and Y position to place the picture. Depending on the size of the picture, you will be asked one or two attributes
1. **Three Nitro files will be created**, ready to be used in Rom Hack

## Notice
If you open a new 16-colors NCGR pictures in [NitroPaint](https://github.com/Garhoogin/NitroPaint), you will find a second transparent part. Ignore it.

## Fun Facts
- A 16-colors NCGR file share the same format as the GBA. It can be modified in [YY-CHR](https://www.romhacking.net/utilities/119/) with the GBA setting
- A 256-colors palette also works for a 16-colors picture, as seen with Cooking Mama DS

## Results
![Giana Sisters DS - Credit MOD (DSLazy Method)__28380 Zigaudrey Last Screen](https://github.com/zigaudrey/DS-nitro-file-builder/assets/129554573/f14ccaf7-66cd-46aa-8c34-f28dbba3b0cc)
< 256-colors (Giana Sisters DS)
![WarioWare DIY - Tech Savvy Guy Splash Screen__27382](https://github.com/zigaudrey/DS-nitro-file-builder/assets/129554573/31c7fcad-7a5b-4207-bebc-16d911ff8701)
< 16-colors (WarioWare: Do It Yourself)

## Sources
Many DS games, their files and [GBATek](http://problemkaputt.de/gbatek-ds-files-2d-video.htm)

This script is sufficient to have the picture display on DS.
