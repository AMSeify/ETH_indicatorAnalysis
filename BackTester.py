from ast import Str


class Tester:
    """this Class get pandas DataFram and Backtest the strategy
        Clearly make the winrate by persent
    """
    def __init__(self , dataframe , BuyCol , SellCol) -> None:
        
        """import the pandas DF and clear which columns is
            Buy/Sell Open and which one is Buy/Sell Stops

        Args:
            dataframe (pandas.dataframe): pandas dataframe that implement 
            the strategy on it (mostly it download on yahoo finance by yfinance module)
            
            BuyCol (Str): name of the Buy Column
            
            SellCol (Str): name of the Buy Column
        """
        self.df = dataframe
        self.BuyCol = BuyCol
        self.SellCol = SellCol


