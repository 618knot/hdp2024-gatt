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
        """doc
        MCP3008にあったアナログ入力を取得するメソッド
        ※MCP3008の分解能は10bit

        Args:
            channel (int): MCP3008のチャンネル。mcp3008からCH名を呼び出せる ex) mcp3008.CH0 -> 8

        Var:
            value (list): 長さ1のリスト。リストの中身は0~1023の値

        Returns:
            float: valueを0~1の値で表現したもの
        """
        value = self.adc.read([channel])
        
        return # write your code here.

if __name__ == "__main__":
    import time
    j = Joystick()

    try:
        while True:
            print(j.get_values())
            time.sleep(1)
    finally:
        j.close()    
        