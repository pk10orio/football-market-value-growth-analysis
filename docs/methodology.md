# Methodology

## Objective

The objective of this project is to estimate which football clubs generated the most player market value between 2013 and 2023.

The project does not attempt to prove direct causality. Instead, it uses player valuation history to identify periods in which players were associated with clubs and measures how their market value changed during those periods.

## Data

The project uses two main files from the Kaggle Transfermarkt dataset:

- `player_valuations.csv`: historical market value records.
- `players.csv`: player metadata, including player names.

## Processing Steps

1. Player valuation records are loaded from `player_valuations.csv`.
2. Player names are added from `players.csv`.
3. Dates are converted to datetime format.
4. Market values are converted to numeric values.
5. Invalid records without date or market value are removed.
6. The analysis is filtered to the period from 2013 to 2023.
7. Each player's records are sorted chronologically.
8. A new player-club period is identified whenever the player's club changes.
9. For each player-club period, the first and last market values are captured.
10. Absolute and percentage growth are calculated.
11. Results are aggregated at club level.

## Filters

The following filters are applied to reduce noise:

- Player-club periods must last more than 90 days.
- Initial market value must be greater than EUR 100,000.
- Clubs must have at least 5 analyzed players.

## Metrics

`total_value_created`

Total sum of market value growth across all analyzed player-club periods for a club.

`avg_value_created`

Average value created per analyzed player-club period.

`median_value_created`

Median value created per analyzed player-club period.

`avg_growth_pct`

Average percentage growth across analyzed player-club periods.

`players`

Number of unique players analyzed for each club.

`positive_rate`

Share of valid player-club periods where market value increased.

## Interpretation

A club with a high total value created may have developed players, recruited well, benefited from market timing, or held players during periods of strong valuation growth.

A club with a negative total value does not necessarily perform poorly in sporting terms. It may buy expensive established players, hold aging players, or appear in the data during periods of market value decline.

## Limitations

Transfermarkt market values are estimates, not official transaction prices.

The method attributes value changes to the club associated with each valuation period, but external factors can also affect player values, including injuries, national team performance, league reputation, age, contract status, and general market inflation.

