# Capstone project : Does new report or manipulate financial markets? 
#### In collaboration with Canadian housing news outlet Better Dwelling

Introduction: This project aims to  explore the relationship between news article sentiment and economic indicator performance in Canada. The project involved scraping Canadian news articles, assigning polarity classification using a sentiment analyzer, and creating a visualization interface displaying correlation results.


#### Our final product deliverable:
![Dash visualization app interface](https://github.com/amlkteam/capstone/blob/master/readme_img/switch_indicator_graphs.gif)

[Check out our Presentation slides on Model training results, Correlation Analysis and Error Analysis](https://github.com/amlkteam/capstone/blob/master/Better%20Dwelling%20Capstone_Presentation_combined.pdf)

**Programming Pipeline - Three independent modules:**

```
  - /data_extraction
  - /sentiment_analyzer
  - /visualization
```

**Dependency Packages and Libraries:**

|Package| Version|
------:|-------:|
Python| 3.7|
**Flair**| **0.5** |
requests | 2.23.0 |
beautifulsoup4 | 4.9.1 |
pandas | 1.0.2 |
scikit_learn | 0.23.1 |
scipy | 1.4.1 |
dash | 1.10.0 |
plotly | 4.5.4  |

Note: bolded dependency must be the specified version; unbolded ones represent the versions we used and tested.

---------------------------------------------------------------------------------------------------------------------------
### <u>Data Extraction Module:</u>

**1. CBC  article scraping** -- To extract the data from the CBC news site execute the following script

**2. Bloomberg News From Financial Post article scraping** -- To extract the articles from author "Bloomberg News" on Financial Post website

**3. Bloomberg News From BNN Bloomberg article scraping** -- To extract the articles from official website of [BNN Bloomberg](https://www.bnnbloomberg.ca/) 

**4. CBC Sampling for annotation** -- To sample the data from the CBC articles that are extracted to be split into data to_annotate and data to_predict

**5. Bloomberg Sampling for annotation** -- Sample the data from the Bloomberg articles that are extracted.

-----------------------------------------------------------------------------------------------------------------------------

### <u>Sentiment Analyzer Module:</u>

**1. Finetuning Sentiment Analyzer for a specific economic indicator**

**Purpose:** To execute two-stage finetuning on the pretrained general sentiment classifier, with first stage feeding in a general Financial News dataset (combined and balanced from 4000+ examples from [Malo, P., Sinha, A., Korhonen, P., Wallenius, J., & Takala, P. (2014)](https://www.kaggle.com/ankurzing/sentiment-analysis-for-financial-news), and 500 + examples from [Matheus Gomes de Sousa et. al](https://drive.google.com/file/d/1eqNwkqb1tnaJm_l975K6LJBic8pMof1x/view)), and second stage feeding in Canadian specific financial news datasets that we have labelled (~600 examples).

**Oversampling and undersampling:** Oversampling and undersampling are techniques used to adjust the class distribution of a dataset. We conducted oversampling by randomly sampling the under-represented classes with replacement, and undersampling by randomly sampling the over-represented classes. For our experiment, we used the undersampling method for the datasets of employment and stock market, and implemented the oversampling method for the datasets of the rest four economic indicators.

#### We inject human knowledge/understanding of the economic/financial world through annotated/golden-labelled examples to train more accurate indicator-specific models.  
Factors we took into consideration when labelling sentiment of news articles with respect to each economic indicator:

 Economic Indicator | Factors that influence the economic indicator
 -------------------------------------------------------------------
 GDP  | Employment, Economy, Investment in a company, Layoffs, Province-level increase/decrease.  
 Employment | Recession, Layoffs, Investment in a large company.
Stock Market | Interest rates, Employment, General economy
Interest rate | Economy, Employment, Inflation target
Mortgage rate | Interest rate as a cost of funding, Bank competition(price war to gain market share), Lay offs, Economy, Housing price
Housing price | Economy, Insolvency/bankruptcy (leads to force sale ),investment by a big company, Surge in investors, Money laundering(push up certain luxury housing price), Layoffs(if it increases insolvency rate of home owners, likely if big layoffs)

#### Model training results
- baseline pretrained Bert models only gave accuracy around 0.5-0.6 when doing sentiment classification on our golden-labelled test-set
Classifier | Best Accuracy | Best F1-score
------------------------------------------
GDP | 0.82 | 0.72
Mortgage Rate | 0.72 | 0.56
Interest Rate| 0.83 | 0.70
Employment | 0.75 | 0.64
Housing Price | 0.74 | 0.62
Toronto Stock Exchange Index | 0.83 |0.75


**2. Make predictions on news articles** -- Make predictions on news articles based on title and subtitles

**3. Calculate final sentiment values** -- Calculate the final sentiment score for all the predicted data points, and combine them with annotated data point to a csv file, that will function as the input for visualization

-----------------------------------------------------------------------------------------------------------------------

### <u>Visualization Module:</u>

**1. Build combined indicator datafile for visualization** -- To extract relevant values from indicator data files and combine into one csv file. 

**2. Run final visualization** -- To visualize the correlation between changes in news sentiment against trend in economic indicator with Plotly in a Dash app.

------------------------------------------------------------------------------------------------------------------------
### Challenges and errors:

The results of the project resulted in 5 out of the 6 models finding positive correlation for the time period observed. GDP was found to have the most heavy positive correlation with the collected news sources, while only mortgage rates were found to have a negative correlation when considering averaged monthly news sentiment. 

Main issues with classification include: news reporting practices creating bias towards negative or neutral classifications, ambiguity in classifying on title and description text alone, and overall small dataset size for fine-tuning. 

Future work for this project can address improvements to classification accuracy by expanding manual annotation datasets and re-working classification pipeline to assign polarity score based on full text content.


