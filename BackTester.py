import pandas as pd

class Tester:
    """this Class get pandas DataFrame and Backtest the strategy
        Clearly make the winrate by persent
    """
    def __init__(self , dataframe ) -> None:
        
        """import the pandas DF and clear which columns is
            Buy/Sell Open and which one is Buy/Sell Stops

        Args:
            dataframe (pandas.dataframe): pandas dataframe that implement 
            the strategy on it (mostly it download on yahoo finance by yfinance module)
            
            BuyCol (Str): name of the Buy Column
            
            SellCol (Str): name of the Buy Column
        """
        self.df = dataframe
        self.money = 100
        self.BadRecords = pd.DataFrame.from_dict({
            "time": [],
            "profit" : [],
            "position" : []
        })
        
    def persentBacktester(self , BuyCol , SellCol):
        """this method Calculate the strategy profit by persent

        Returns:
            float64: total persent of the strategy %
        """
        self.BuyCol = BuyCol
        self.SellCol = SellCol
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
                
        return persent -100
    
    def badrecords(self):
        """this Method sent the worst position to debug the strategy

        Returns:
            pandas.dataframe: this Dataframe include worst trade for backtest
        """
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
    
    def SigMixer(self, ins, start, end):
        """this method make Clear signal from boolean multiple Series

        Args:
            ins (pandas.Series): this is simple instance signal and instance signal must be
            always true to continue the trade
            start (pandas.Series): when the start series rich to True signal will start :)
            end (pandas.Series): when the stop series rich to True the main signal will stops

        Returns:
            pandas.Series: the main signal
        """
        startindex = None
        endindex = None 
        Is_StartFound = False
        self.df["sig"] = False
        signal = self.df.sig
        for index in ins.index:
            # print(start[index])
            if ins[index] & start[index] & ~Is_StartFound:
                startindex = index
                Is_StartFound = True
            elif ins[index] & end[index]:
                endindex = index
        signal[startindex:endindex] = True
        return signal

import yfinance as yf
import pandas_ta as ta

ETH = yf.download(tickers="XRP-USD" , interval="5m" , period="25h")
ETH["EMA10"] = ta.ema(ETH.Close , 10)
ETH["EMA15"] = ta.ema(ETH.Close , 15)
ETH["EMA20"] = ta.ema(ETH.Close , 20)

ETH.dropna(inplace=True)

ETH["Buy"] = (ETH.EMA5 > ETH.EMA8) & (ETH.EMA8 > ETH.EMA13) #& (ETH.MACD > 0 )
ETH["Sell"] = (ETH.EMA5 < ETH.EMA8) & (ETH.EMA8 < ETH.EMA13) #& (ETH.MACD < 0 )

ETH_tester = Tester(ETH)

ETH["MACD"] = ta.macd(ETH.Close ,12,26,9)["MACDh_12_26_9"] > 0
# print(type(stop))
ETH["FinalBuy"] = ETH_tester.SigMixer(ETH.Buy , ETH.MACD ,~ETH.Buy)
ETH["FinalSell"] = ETH_tester.SigMixer(ETH.Sell , ~ETH.MACD ,~ETH.Sell)
# print(ETH.FinalBuy)

print(ETH_tester.persentBacktester("Buy" , "Sell"))

print(ETH_tester.persentBacktester("FinalBuy" , "FinalSell"))