import pandas as pd

class Tester:
    """this Class get pandas DataFrame and Backtest the strategy
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
        self.money = 100
        self.BadRecords = pd.DataFrame.from_dict({
            "time": [],
            "profit" : [],
            "position" : []
        })
        
    def persentBacktester(self):
        persent = self.money
        buy = False
        sell = False
        
        for index in self.df.index:
            if (self.df.Buy[index] == True) & (buy == False):
                s= self.df.Close[index]
                buy =True
                
            elif (self.df.Buy[index] == False) & (buy == True):
                persent *= 1 +((self.df.Close[index]-s)/s)
                buy = False
                
            elif (self.df.Sell[index] == True) & (sell == False):
                s= self.df.Close[index]
                sell =True
                
            elif (self.df.Sell[index] == False) & (sell == True):
                persent *= 1 +(-1* (self.df.Close[index]-s)/s)
                sell = False
                
        return persent
    
    def badrecords(self):
        br = self.BadRecords
        # persent = 1
        buy = False
        sell = False
        
        for index in self.df.index:
            if (self.df.Buy[index] == True) & (buy == False):
                s= self.df.Close[index]
                buy =True
                
            elif (self.df.Buy[index] == False) & (buy == True):
                persent = (self.df.Close[index]-s)/s * 100
                if persent < 0.09 :
                    br.loc[len(br.index)]={"time": index,
                                "profit" : persent,
                                "position" : "Buy"
                                }
                buy = False
                
            elif (self.df.Sell[index] == True) & (sell == False):
                s= self.df.Close[index]
                sell =True
                
            elif (self.df.Sell[index] == False) & (sell == True):
                persent = (-1* (self.df.Close[index]-s)/s) * 100
                if persent <0.09 :
                    br.loc[len(br)] = {"time":index,
                                "profit" : persent,
                                "position" : "Sell"
                                }
                sell = False
        return br


# first test of the Backtest Proccess
# The EMA Algorithm

import yfinance as yf
import pandas_ta as ta

ETH = yf.download(tickers="ETH-USD" , interval="5m" , period="30d")
ETH["EMA5"] = ta.ema(ETH.Close , 5)
ETH["EMA8"] = ta.ema(ETH.Close , 8)
ETH["EMA13"] = ta.ema(ETH.Close , 13)
ETH.dropna(inplace=True)

ETH["Buy"] = (ETH.EMA5 > ETH.EMA8) & (ETH.EMA8 > ETH.EMA13)
ETH["Sell"] = (ETH.EMA5 < ETH.EMA8) & (ETH.EMA8 < ETH.EMA13)

ETH_tester = Tester(ETH , "Buy" , "Sell")
# print(ETH_tester.BadRecords)
ETH_tester.badrecords().sort_values("profit").to_csv("BadRecords.csv")

ETH[(ETH.Buy==True) | (ETH.Sell == True)].to_csv("ETH5min_3eyes.csv")