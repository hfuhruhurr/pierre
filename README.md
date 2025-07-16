## BTC-USD Price History Data Sources

Interestingly, there doesn't seem to be a consensus source for daily price action.

It should be noted that BTC trading didn't even begin until June/July 2010.  Thus, don't expect data prior to that.  (Unless you go the UTXOracle route, but I digress.)

### Pierre

* How to obtain:
    * ??? source unverified
* Earliest date: 1/1/2010 (implicitly)
### Coingecko

* How to obtain:
    * Go to [coingecko](https://www.coingecko.com/en/coins/bitcoin/historical_data)
    * Click on `Max` (to reveal entire price history)
    * Click on the downloand icon (to download the data)
* Earliest date: 4/28/2013
* Missing dates: 6/4/2013, 1/28/2015

### Federal Reserve 

* How to obtain:
    * Go to [the Federal Reserve](https://fred.stlouisfed.org/series/CBBTCUSD)
    * Click on `Max` (to reveal entire price history)
    * Click on `Downloand` (to download the data)
* Earliest date: 12/1/2014
* Missing dates: It does have 1/28/2015 but is missing 35 others, only 1 after 1/19/2015.

### Investing.com
* How to obtain:
    * https://www.kaggle.com/datasets/shiivvvaam/bitcoin-historical-data
* Earliest date: 7/18/2010
* Latest date: 2/9/2024
* Missing dates: none
* Weird:  data has `Price`, `Open`, `High`, and `Low` columns.  No `Close`.  Thus, one would assume `Price` = `Close` and `Close` = tomorrow's `Open`...but this isn't the case for about 1/3 of the records.  Granted, the magnitude of the deltas are tiny enough to not materially affect decisions but it's frustrating to realize this lack of care in someone's data.