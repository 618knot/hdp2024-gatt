import mcp3008

class Joystick:
    def __init__(self) -> None:
        self.x_ch = mcp3008.CH1
        self.y_ch = mcp3008.CH0
        self.adc = mcp3008.MCP3008()
        
    def get_values(self):
        input_x = self.__analog_read(self.x_ch)
        input_y = self.__analog_read(self.y_ch)
        
        return { "x": input_x, "y": input_y }

    def close(self):
        self.adc.close()

    def __analog_read(self, channel):
        value = self.adc.read([channel])
        
        return value.pop() / 1024
