# Optimizing Book Exchange Inventory and Promotion Strategy Based on Popularity, Ratings, and Market Trends

## Repository Outline
1. P0M1_clarence_manzo.ipynb - Notebook to load data, explore data, preprocessed data, and analyze data
2. P0M1_clarence_manzo_dataset.csv - Raw dataset straight from the source
3. P0M1_clarence_manzo_dataset_cleaned.csv - Cleaned dataset that is used for analyzing
4. README.md - Summary description about the project
5. assignment-rubrics.png - Image containing assignment rubric
6. description.md - Repository project description and documentation

## Problem Background
A book-exchange platform operates by matching supply (available books) with demand (books requested for swapping) across different countries. However, the platform currently lacks data-driven insights to determine which books should be prioritized for inventory acquisition, promotion, and regional marketing.

With a large dataset containing book attributes such as genre, ratings, publication year, bestseller status, and movie adaptations, there is an opportunity to uncover demand patterns and optimize business decisions.

## Project Output
Dashboard data visualization and analysis using Tableau Public and Python Notebook.

## Data
The dataset is taken from the Kaggle Website. The dataset titled “The Most Popular Books for Exchanging” contains information on books that are frequently requested or swapped on a book-exchange platform. Each record represents a single book with complete descriptive and popularity indicator information.

Column Descriptions:
- id (Integer): A unique ID for the record.
- title (String): Book's title.
- author (String): Author's name.
- genre (String): Book's genre.
- language (String): The language in which the book is written or published.
- publicationYear (Integer): Book's published year.
- publisher (String): Publisher's name.
- description (String): The book's synopsis.
- pageCount (Integer): The total number of pages in the book.
- tags (String): Comma-separated keywords or tags describing the book's themes.
- rating_average (Float): The average user rating.
- most_popular_country (String): The country where the book is most requested.
- bestseller_status (Boolean): A recognized bestseller book or not.
- awards (String): A list of awards the book has won.
- age_category (String): The target age group.
- adapted_to_movie (Boolean): The book has been adapted into a film or not.
- movie_release_year (Float): The year the movie adaptation was released.
- isbn (String): The International Standard Book Number, a unique numeric commercial book identifier.

The dataset contains 990 records of book with 18 columns/attributes.

Column awards has 600 missing values and column movie_release_year has 350 missing values, the rest of the columns don't have missing values.

Number of unique values:
- id                     : 990
- title                  : 990
- author                 : 555
- genre                  : 81
- language               : 13
- publicationYear        : 175
- publisher              : 297
- description            : 990
- pageCount              : 457
- tags                   : 968
- rating_average         : 125
- most_popular_country   : 39
- bestseller_status      : 2
- awards                 : 128
- age_category           : 3
- adapted_to_movie       : 2
- movie_release_year     : 95
- isbn                   : 986

## Method
statistic descriptive: central tendency & measure of variance

statistic inferential: hypothesis testing with two-sample t-test

## Stacks
Programming langugage: Python

Tools: Visual Studio Code and Tableau Public

Library: pandas, numpy, scipy, and matplotlib.pyplot

## Reference
Dataset URL: https://www.kaggle.com/datasets/sergiykovalchuck/the-most-popular-books-for-exchanging?resource=download

Dashboard URL: https://public.tableau.com/app/profile/clarence.manzo/viz/P0M1_clarence_manzo/BookExchangeInsightsDashboard?publish=yes






