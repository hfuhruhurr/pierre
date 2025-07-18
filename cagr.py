import marimo

__generated_with = "0.14.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    import numpy as np
    from datetime import datetime
    return np, pl, plt


@app.cell
def _(pl):
    cg = (
        pl.read_csv('Coingecko BTC-USD Daily.csv')
        .with_columns(
            pl.col("snapped_at").str.strptime(pl.Date, "%Y-%m-%d %H:%M:%S %Z")
        )
        .rename({"snapped_at": "date"})
    )
    return (cg,)


@app.cell
def _(pl):
    cb = (
        pl.read_csv('Coinbase BTC-USD Daily.csv')
        .with_columns(
            pl.col("observation_date").str.strptime(pl.Date, "%Y-%m-%d")
        )
        .drop_nulls()
        .rename({
            "observation_date": "date",
            "CBBTCUSD": "price"
        })
    )
    return (cb,)


@app.cell
def _(pl):
    investing = (
        pl.read_csv('Investing.com BTC-USD Daily.csv')
        .with_columns(
            pl.col("Date").str.strptime(pl.Date, "%b %d, %Y"),
            pl.col("Price").str.replace(",", "").cast(pl.Float64),
            pl.col("Open").str.replace(",", "").cast(pl.Float64),
            pl.col("High").str.replace(",", "").cast(pl.Float64),
            pl.col("Low").str.replace(",", "").cast(pl.Float64)
        )
        .drop(["Vol.", "Change %"])
        .drop_nulls()
        .rename(lambda col: col.lower())
        .sort("date", descending=True)  # Ensure date order
    )
    return (investing,)


@app.cell
def _(pl):
    def reveal_missing_dates(df: pl.DataFrame, date_col: str='date', price_col: str='price') -> pl.DataFrame:
        max_date = df[date_col].max() 
        min_date = df[date_col].min()

        all_dates = pl.DataFrame({
            "date": pl.date_range(
                start=min_date,
                end=max_date,
                interval='1d',
                eager=True
            )
        })

        return (
            all_dates
                .join(df, on=date_col, how='left')
                .filter(pl.col(price_col).is_null())
        )
    return (reveal_missing_dates,)


@app.cell
def _(cg, reveal_missing_dates):
    reveal_missing_dates(cg)
    return


@app.cell
def _(cb, reveal_missing_dates):
    reveal_missing_dates(cb)
    return


@app.cell
def _(investing, reveal_missing_dates):
    reveal_missing_dates(investing)
    return


@app.cell
def _(pl):
    def calculate_horizon_cagrs(df: pl.DataFrame, horizon_days: int=365):
        # df can have any number of fields, as long as it has "date" and "price"

        # Set the rolling window size
        p = f'{horizon_days}d'

        # Build a df of all the possible CAGRs
        cagrs = (
            df
            # Bulletproof df
            .sort(by='date')

            # Create needed columns
            .with_columns(
                pl.first('date').rolling(index_column='date', period=p).alias('invest_date'),
                pl.first('price').rolling(index_column='date', period=p).alias('invest_price'),
                pl.last('date').rolling(index_column='date', period=p).alias('mature_date'),
                pl.last('price').rolling(index_column='date', period=p).alias('mature_price'),
                pl.count('price').rolling(index_column='date', period=p).alias('n_obs'),
            )

            # Keep relevant columns
            .select(['invest_date', 'invest_price', 'mature_date', 'mature_price'])

            # Gather potentially interesting stat (# of data days in rolling window)
            .with_columns(
                ((pl.col('mature_date') - pl.col('invest_date')).dt.total_days() + 1).alias('n_days')
            )

            # Discard truncated rolling windows
            .filter(
                pl.col('n_days') == horizon_days
            )

            # Calculate CAGR
            .with_columns(
                ((pl.col('mature_price') / pl.col('invest_price'))**(365 / pl.col('n_days')) - 1).alias('cagr')
            )
        )

        min_date = cagrs['invest_date'].min()
        max_date = cagrs['mature_date'].max()
        median_cagr = cagrs['cagr'].median()

        worst_case = (
            cagrs
            .filter(
                pl.col('cagr') == pl.min('cagr')
            )
        )

        if len(worst_case):
            worst_case_invest_date = worst_case['invest_date'][0]
            worst_case_cagr = worst_case['cagr'][0]
        else:
            return horizon_days / 365.0, None, None, None 

        return (
            horizon_days / 365.0, 
            worst_case_invest_date, 
            100 * worst_case_cagr, 
            100 * median_cagr, 
            min_date, 
            max_date
        )

    return (calculate_horizon_cagrs,)


@app.cell
def _(calculate_horizon_cagrs, pl):
    def build_cagrs_df(prices: pl.DataFrame) -> pl.DataFrame:
        data = [
            calculate_horizon_cagrs(prices, h)
            for h in range(365, 11*365 + 1)
        ]

        cagrs =  pl.DataFrame(
            data, 
            schema={
                "horizon": pl.Float64,
                "worst_case_invest_date": pl.Date,
                "worst_case_cagr": pl.Float64,
                "median_cagr": pl.Float64,
                "first_invest_date": pl.Date,
                "last_mature_date": pl.Date,
            },
            orient='row'
        )

        return (
            cagrs 
            .with_columns(
                pl.col('worst_case_invest_date').dt.year().alias('worst_case_invest_year')
            )
        )

    return (build_cagrs_df,)


@app.cell
def _(np, pl, plt):
    def draw_cagr_plot(df: pl.DataFrame, pierre: bool=False):
        # Sort the DataFrame by investment horizon
        df = df.sort('horizon')

        # Get unique years from worst_case_invest_year
        unique_years = df['worst_case_invest_year'].unique().sort()
        num_years = len(unique_years)
        
        # Create discrete colormap: 1 year = 1 color
        colors = plt.cm.Set1(np.linspace(0, 1, num_years))
        year_map = {year: idx for idx, year in enumerate(unique_years)}

        # Create the plot
        plt.figure(figsize=(10, 6))

        if pierre:
            # Pierre's chart
            plt.plot(
                df['horizon'],
                df['worst_case_cagr'],
                color='black',
            )
        else:
            # Dude's chart
            for year in unique_years:
                mask = df['worst_case_invest_year'] == year
                plt.scatter(
                    df.filter(mask)['horizon'],
                    df.filter(mask)['worst_case_cagr'],
                    c=[colors[year_map[year]]],
                    label=year,
                    zorder=5,
                    marker='.'
                )

            # Add legend
            plt.legend(title='Investment Year', loc='lower right')

        # Title
        plt.suptitle('Worst Case CAGR by Investment Horizon')
        min_date = df['first_invest_date'][0]
        max_date = df['last_mature_date'][0]
        title = f"Data from {min_date} thru {max_date}"
        title += "\nSource: Coingecko"
        plt.title(title, x=0.01, ha='left', fontsize=8)

        # Labels
        plt.xlabel('Investment Horizon (Years)')
        plt.ylabel('Worst Case CAGR')

        # Y-ticks formatted as percentages
        yticks = range(-100, 70, 10)
        plt.yticks(yticks, [f'{val}%' for val in yticks])
        plt.grid(True, axis='x', linestyle='-', alpha=0.7)

        # X-ticks
        xticks = range(1, 12)
        plt.xticks(xticks, [f'{val} y' for val in xticks])

        # Limits and grid
        plt.xlim(0.5, 11.5)
        plt.ylim(-105, 65)
        plt.grid(True, axis='y', linestyle='-', alpha=0.7)

        # Show the plot
        plt.tight_layout()
        plt.show()
    return (draw_cagr_plot,)


@app.cell
def _(build_cagrs_df, cg):
    dude = build_cagrs_df(cg)
    return (dude,)


@app.cell
def _(draw_cagr_plot, dude):
    draw_cagr_plot(dude, False)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
