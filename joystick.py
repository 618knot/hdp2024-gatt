from gpiozero import MCP3008

class Joystick:
    def __init__(self, x_ch = 1, y_ch = 0) -> None:
        self.x_ch = x_ch
        self.y_ch = y_ch
        
    def get_values(self):
        input_x = self.__analog_read(self.x_ch)
        input_y = self.__analog_read(self.y_ch)
        
        return { "x": input_x, "y": input_y }

    def __analog_read(self, channel):
        pot = MCP3008(channel)
        value = pot.value
        
        return value
