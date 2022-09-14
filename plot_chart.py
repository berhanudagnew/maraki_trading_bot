import plotly.graph_objects as go
class PlotChart:
    def __init__(self, _data):
        self.data = _data
    def view(self):
        fig = go.Figure(data=[go.Candlestick(x = self.data['date'],
                        open=self.data['open'],
                        high=self.data['high'],
                        low=self.data['low'],
                        close=self.data['close'],
                        )])
        fig.show()