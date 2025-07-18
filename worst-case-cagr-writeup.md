+++
date = '2025-07-17T15:27:27-04:00'
draft = true
title = 'Worst Case Cagr'
tags = 'bitcoin' 'replicate'
+++

## Motivation
On July 15, 2025, Pierre Rochard posted this on X:
https://x.com/BitcoinPierre/status/1945147693308711299

Slick chart. Novel story. Tremendous interpretation.  But is it true?

I am going to replicate the chart to:
1. Convince myself the chart is correct
2. Hone my data nerd skills
3. Reveal the methodology and data sources so anyone can corobborate 

## Understanding the raw data need
The chart data consists of:
1. an investment horizon (x-axis)
2. the worst case CAGR @ that investment horizon (y-axis)

Thus, we are plotting:

| horizon | min_cagr | 
| :-: | :-: |
| 1.0000 | -83.64 | 
| 1.0027 | -83.53 |
| 1.0054 | -83.47 |
| ... | ... |
| 11.0000 | 49.34 |

To arrive at a minimum CAGR for a particular horizon, we need to consider the CAGR at each possible start date. A table such as this would suit us nicely:
| horizon | start_date | cagr |
| :-: | :-:  | :-: |
| 1.0000 | 2013-04-28  |  2.23 |
| 1.0000 | 2013-04-29  |  2.07 |
| 1.0000 | 2013-04-30  |  2.27 |
| 1.0000 | ... | ... |
| 1.0000 | 2024-07-16  |  0.84 |


We're not given CAGR, we need to calculate it from the raw data.  

The calculation for CAGR is:
$$\left(\frac{\text{price at end of horizon}}{\text{price at start of horizon}}\right)^{\frac{1}{\text{\# of years in horizon}}} - 1$$

This means if we can get the following data then we can derive everything we need:

| horizon | start_date | start_price | end_date | end_price | 
| :-: | :-:  | :-: | :-: | :-: | 
| 1.0000 | 2013-04-28 | 135.3  | 2014-04-27 | 437.92 | 
| 1.0000 | 2013-04-29 | 141.96 | 2014-04-28 | 436.92 | 
| 1.0000 | 2013-04-30 | 135.3  | 2014-04-29 | 443.27 | 
| 1.0000 | ... | ... | ... | ... | ... | 
| 1.0000 | 2024-07-16 | 64835.48 | 2025-07-15 | 119833.67 | 

To populate this table, all we need is:

| date | price |
| :-: | :-: |
| 2013-04-28 | 135.3 |
| 2013-04-29 | 141.96 |
| 2013-04-30 | 135.3 |
| ... | ... |
| 2025-07-15 | 119833.67 |

Pretty straight forward, eh? 

## Source Data
It turns out getting daily USD prices for bitcoin isn't straight forward.

One can find daily USD prices from several sources ([CoinGecko](https://www.coingecko.com/en/coins/bitcoin/), [CoinMarketCap](https://coinmarketcap.com/currencies/bitcoin/), [the Federal Reserve](https://fred.stlouisfed.org/series/CBBTCUSD), [Yahoo! Finance](https://finance.yahoo.com/quote/BTC-USD/history/), [Kaggle via Investing.com](https://www.kaggle.com/datasets/shiivvvaam/bitcoin-historical-data), etc.).  But the all vary in when the data starts and stops.  Most start around 2013...but Pierre's data starts in 2010.

I chose to use CoinGecko's data, even though theirs starts in 2013.

Why?

Because running the analysis with just that data was enough to convince me the chart is accurate.

## Replication
Here ya go:

## Added Flair
What if we added a visual dimension to convey *when* the worse case CAGR occurred?
