import os
import struct

from tkinter import *
from tkinter import filedialog
from math import floor
from PIL import Image

pic_file = ""
pic_file = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select PNG or BMP", filetype=(('PNG file', '*.png'),('BMP file', '*.png'),("ALL file",'*.*')))

NCGR_subsection = b'SOPC\x10\x00\x00\x00\x00\x00\x00\x00\x18\x00\x04\x00'
NCLR_footer = bytearray()
NCGR_subsection = bytearray()

grid = []
grid_line = []

for y in range(24):
    for x in range(32):
        grid_line.append(0)
    grid.append(grid_line)
    grid_line = []

BGR_bin = 0

if len(pic_file) != 0 :

    openpic = Image.open(pic_file).convert("RGB")
    w,h = openpic.size

    NSRC_header = b'RCSN\xFF\xFE\x00\x01\x24\x06\x00\x00\x10\x00\x01\x00NRCS\x14\x06\x00\x00\x00\x01\xC0\x00\x01\x00\x00\x00\x00\x06\x00\x00'
    
    if (w % 8 == 0 and h % 8 == 0) and (w <= 256 or h <= 192) :

        depth = 0

        while depth != 3 and depth !=4:
            depth = int(input("Choose colors depth (3 = 16 Colors, 4 = 256 Colors) "))
            if depth != 3 and depth !=4:
                depth = 0

        gx, gy = -1, -1

        if w // 8 != 32:
            while gx == -1:
                print("Between 0 and", 32 - w//8)
                gx = int(input("Choose X Position: "))
                if gx < 0 or gx > 32 - w //8:
                    gx = -1
        else:
            gx = 0            

        if h // 8 != 24:
            while gy == -1:
                print("Between 0 and", 24 - h //8)
                gy = int(input("Choose Y Position: "))
                if gy < 0 or gy > 24 - h //8:
                    gy = -1
        else:
            gy = 0

        order = 0
        for n in range(h // 8):
            for m in range(w // 8):
                grid[gy + n][gx + m] = order
                order += 1

        bit_paint = bytearray()
        pal_bin = bytearray()

        short_file_name = ""

        n=len(pic_file)-5
        while n!= 0 and pic_file[n] != '/':
            short_file_name = pic_file[n] + short_file_name
            n -= 1
                    
        pic_name = short_file_name + ".NCGR"
        pal_name = short_file_name + ".NCLR"
        grid_name = short_file_name + ".NSCR"
                
        byte_C = 0

        list_colors = [(0,0,8)]
        R, G, B = list_colors[-1]
        R, G, B = floor(R // 8), floor(G // 8), floor(B // 8)
        RGB = (R, G, B)
        pal_bin += struct.pack("<L", (B * 32 * 32) + (G * 32) + R )[:2]

        if depth == 3 :
            more_than_16 = False
            
            for y in range(0, h, 8):
                for x in range (0, w, 8):
                    for iz in range(0, 8):
                        for ix in range(0, 8, 2):
                            RGB, RGB2 = openpic.getpixel((x+ix,y+iz)) , openpic.getpixel((x+ix+1,y+iz))
                            R, G, B = RGB
                            R, G, B = floor(R // 8), floor(G // 8), floor(B // 8)
                            RGB = (R, G, B)
                            R2, G2, B2 = RGB2
                            R2, G2, B2 = floor(R2 // 8), floor(G2 // 8), floor(B2 // 8)
                            RGB2 = (R2, G2, B2)
                            if len(list_colors) < 16:
                                if not RGB in list_colors:
                                    list_colors.append(RGB)
                                    pal_bin += struct.pack("<L", (B * 32 * 32) + (G * 32) + R )[:2]
                                if not RGB2 in list_colors:
                                    list_colors.append(RGB2)
                                    pal_bin += struct.pack("<L", (B2* 32 * 32) + (G2 * 32) + R2 )[:2]
                            b1, b2 = 0 , 0
                            if RGB in list_colors:
                                b1 = list_colors.index(RGB)
                            if RGB2 in list_colors:
                                b2 = list_colors.index(RGB2)
                            if more_than_16 == False and len(list_colors) == 16 and (not RGB in list_colors or not RGB2 in list_colors):
                                more_than_16 = True
                                print("This Picture has more than 16 colors")
                            bin_color = struct.pack("B", b2 * 16 + b1)
                            bit_paint += bin_color

        else:

            more_than_256 = False
                
            for y in range(0, h, 8):
                for x in range (0, w, 8):
                    for iz in range(0, 8):
                        for ix in range(0, 8):
                            RGB = openpic.getpixel((x+ix,y+iz))
                            R, G, B = RGB
                            R, G, B = floor(R // 8), floor(G // 8), floor(B // 8)
                            RGB = (R, G, B)
                            if len(list_colors) < 256:
                                if not RGB in list_colors:
                                    list_colors.append(RGB)
                                    pal_bin += struct.pack("<L", (B * 32 * 32) + (G * 32) + R )[:2]
                            byte_C = 0
                            if RGB in list_colors:
                                byte_C = list_colors.index(RGB)
                            if more_than_256 == False and len(list_colors) == 256 and not RGB in list_colors:
                                more_than_256 = True
                                print("This Picture has more than 256 colors")
                            bin_color = struct.pack("B", byte_C)
                            bit_paint += bin_color

        pal_padding_len = 256 - (len(pal_bin) // 2)

        for n in range ( pal_padding_len ):
            pal_bin += b'\xFF\x7F'

        NCLR_header = b'RLCN\xFF\xFE\x00\x01' + struct.pack("<L", len(pal_bin) + 40) + b'\x10\x00\x01\x00TTLP' + struct.pack("<L", len(pal_bin) + 24) + struct.pack("<L", depth ) + b'\x00\x00\x00\x00' + struct.pack("<L", len(pal_bin)) + b'\x10\x00\x00\x00'

        NCGR_subsection = b'SOPC\x10\x00\x00\x00\x00\x00\x00\x00\x20\x00' + struct.pack("<L", h * w )[:2]

        NCGR_size = struct.pack("<L", 64 + len(bit_paint))[:2]
        NCGR_header = b'RGCN\xFF\xFE\x00\x01' + NCGR_size + b'\x00\x00\x10\x00\x01\x00RAHC\x20\x18\x00\x00' + struct.pack("<L", h // 8 )[:2] + struct.pack("<L", w // 8 )[:2] + struct.pack("<L", depth ) + b'\x00\x00\x00\x00\x00\x00\x00\x00' + struct.pack("<L", w * h ) + b'\x18\x00\x00\x00' 
        
        NTFS_data = bytearray()

        for j in range(len(grid)):
            for i in range(len(grid[j])):
                NTFS_data += struct.pack("<L", grid[j][i])[:2]
                
        out_file_pic, out_file_pal, out_file_grid = open(pic_name, "wb+"), open(pal_name, "wb+"), open(grid_name, "wb+")
        out_file_pic.write(NCGR_header + bit_paint + NCGR_subsection) 
        out_file_pal.write(NCLR_header + pal_bin)
        out_file_grid.write(NSRC_header + NTFS_data)
        out_file_pic.close()
        out_file_pal.close()
        out_file_grid.close()

        print("All Three Nitro Files done!")
        
    else:
        if w > 256 or h > 192:
            print("The picture is over 256 x 192")
        else:
            print("The picture doesn't have values that are divisible by 8")

else:
    print("No Picture File Selected")
