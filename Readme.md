# Video Game Sales Analysis

## Background & Overview

The global video game market spans thousands of titles, publishers, and platforms, making it difficult for stakeholders — publishers, platform holders, or marketing teams — to quickly identify which titles, genres, and consoles actually drive sales. This project analyzes historical video game sales data (title, console, genre, publisher, developer, critic score, and regional sales) to uncover which games and genres perform best, and to explain apparent contradictions in the data (e.g., why a single title can outsell an entire genre).

The analysis focuses on:
- Top-performing titles, genres, and consoles by sales
- Title–console and genre–console sales combinations
- A deep dive into why GTA V, an Action title, outsells titles in the higher-grossing Sports genre

For the full analysis code, see [`game_sales.py`](./game_sales.py).

## Data Structure Overview

The dataset (`vgchartz-2024.csv`) contains one row per title-console release, with the following key fields:

| Column | Description |
|---|---|
| `title` | Game title |
| `console` | Console the game was released for |
| `genre` | Genre of the game |
| `publisher` / `developer` | Publisher and developer of the game |
| `critic_score` | Metacritic score (out of 10) |
| `total_sales` | Global sales of copies (millions) |
| `na_sales`, `jp_sales`, `pal_sales`, `other_sales` | Regional sales (millions) |
| `release_date` | Date the game was released |

**Note:** A single title can appear multiple times across different consoles, and in some cases is tagged with different genres across releases — this is treated as valid (title + console is the unit of analysis), not deduplicated.

## Executive Summary

- **GTA V is the best-selling title overall**, despite **Sports being the best-selling genre** — the two findings aren't contradictory: Sports sales are the sum of many titles releasing every year (e.g., annual sports franchises), while GTA V's total comes from a single title with exceptional performance.
- Action and Sports together account for the majority of sales among the top 5 genres (Sports, Action, Shooter, Misc, Racing).
- Sales concentration differs sharply by genre: the Sports genre's top-20 titles show a gradual sales drop-off, while the Action genre shows one extreme outlier (GTA V) far above the rest of the pack.

## Insights Deep Dive

**Genre-level sales are driven by title volume, not just individual title strength.**
Sports ranks #1 by total genre sales, but no single sports title comes close to GTA V's individual sales. This points to a "many good sellers" pattern for Sports versus a "one blockbuster" pattern for Action.

**GTA V's dominance holds across consoles.**
Breaking down GTA V's sales by console (vs. the top Sports title) shows its lead isn't concentrated on one platform — it performs strongly across multiple console releases, reinforcing that its total sales reflect broad, sustained demand rather than a single-platform spike.

**Console–genre combinations reveal platform specialization.**
Looking at top console–genre sales combinations highlights which consoles over-index on specific genres, useful for platform-specific marketing or bundling decisions.

## Recommendations

- **For publishers evaluating genre investment:** Sports remains a reliable, high-volume genre — but expect returns to come from a broad catalog of annual titles rather than single blockbuster releases. Budget and marketing plans should reflect this "volume" strategy rather than expecting one Sports title to match GTA V-level sales.
- **For marketing teams:** Since GTA V-style outliers exist in the Action genre, marketing spend for Action titles should be evaluated per-title rather than genre-wide, since genre averages can be misleading when one title skews the distribution.
- **For platform/console teams:** Use console–genre sales patterns to guide exclusive content or bundling deals — consoles that already over-index on a genre are a natural fit for further genre-specific titles.

## Caveats and Assumptions

- Missing `developer` values were filled as `"Unknown"`; missing regional/total sales were filled as `0`, assumed to represent no recorded sales rather than missing data.
- `release_date` values that couldn't be parsed were coerced to null (`NaT`) rather than dropped.
- Some titles have inconsistent genre labels across console releases (e.g., "Action" vs. "Action-Adventure" for the same title); these were treated as distinct genre tags rather than merged, which may slightly inflate genre-level totals for closely related genres.
- Sales figures are lifetime cumulative totals, not annual figures — trend-over-time claims (e.g., "genre X is growing") cannot be made from this dataset alone.