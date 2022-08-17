import uos
import machine
import time
import st7789py as st7789
import vga2_8x8 as font1
import vga1_16x32 as font2
import displaycolors as Colors


class DisplayUtility():
    
    def __init__(self):
        spi1_sck=10
        spi1_mosi=11
        spi1_miso=8 
        st7789_res = 12
        st7789_dc  = 13
        disp_width = 240
        disp_height = 240
        CENTER_Y = int(disp_width/2)
        CENTER_X = int(disp_height/2)

        print(uos.uname())
        spi1 = machine.SPI(1, baudrate=40000000, polarity=1)
        print(spi1)
        self._display = st7789.ST7789(spi1, disp_width, disp_width,
                              reset=machine.Pin(st7789_res, machine.Pin.OUT),
                              dc=machine.Pin(st7789_dc, machine.Pin.OUT),
                              rotation=0)
        time.sleep(1)
        
        
    
    def WriteLine(self, line):
        self._display.fill(Colors.BLACK)
        start_x=10
        start_y=10
        self._display.text(font2, line, start_x, start_y)

    def WriteLines(self, lines, color = Colors.WHITE, background = Colors.BLACK):
        self._display.fill(background)
        start_x = 10
        start_y = 10
        yspace = font2.HEIGHT + 2        
        
        start_y = int((240- (len(lines) * font2.HEIGHT) )/2)
        
        for line in lines:        
            start_x = int((240- (len(line) * font2.WIDTH) )/2)
            self._display.text(font2, line, start_x, start_y, color, background)
            start_y += yspace + 1
        
    
