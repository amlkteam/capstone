# better_dwelling_capstone
 ---

### Capstone project: Does new report or manipulate financial markets? 


![Dash visualization app interface](https://github.com/amlkteam/capstone/blob/master/readme_img/switch_indicator_graphs.gif)

[Check out our Presentation slides on Model training results, Correlation Analysis and Error Analysis](https://github.com/amlkteam/capstone/blob/master/Better%20Dwelling%20Capstone_Presentation_combined.pdf)

**Pipeline - Three independent modules:**

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

**1. CBC  article scraping**

**Purpose:** To extract the data from the CBC news site execute the following script

**2. Bloomberg News From Financial Post article scraping**

**Purpose:** To extract the articles from author "Bloomberg News" on Financial Post website execute the following script

**3. Bloomberg News From BNN Bloomberg article scraping**

**Purpose:** To extract the articles from official website of [BNN Bloomberg](https://www.bnnbloomberg.ca/) execute the following script

**4. CBC Sampling for annotation**

**Purpose:** To sample the data from the CBC articles that are extracted to be split into data to_annotate and data to_predict


**5. Bloomberg Sampling for annotation**

**Purpose:** Sample the data from the Bloomberg articles that are extracted. The dataset to be used for annotation will be generated, the rest of the articles will be used for prediction. 
-----------------------------------------------------------------------------------------------------------------------------

### <u>Sentiment Analyzer Module:</u>

**1. Finetuning Sentiment Analyzer for a specific economic indicator**

**Purpose:** To execute two-stage finetuning on the pretrained general sentiment classifier, with first stage feeding in a general Financial News dataset (combined and balanced from 4000+ examples from [Malo, P., Sinha, A., Korhonen, P., Wallenius, J., & Takala, P. (2014)](https://www.kaggle.com/ankurzing/sentiment-analysis-for-financial-news), and 500 + examples from [Matheus Gomes de Sousa et. al](https://drive.google.com/file/d/1eqNwkqb1tnaJm_l975K6LJBic8pMof1x/view)), and second stage feeding in Canadian specific financial news datasets that we have labelled (~600 examples).

**Oversampling and undersampling:** Oversampling and undersampling are techniques used to adjust the class distribution of a dataset. We conducted oversampling by randomly sampling the under-represented classes with replacement and undersampling by randomly sampling the over-represented classes. For our experiment, we used the undersampling method for the datasets of employment and stock market, and implemented the oversampling method for the datasets of the rest four economic indicators.

**2. Make predictions on news articles you want to check sentiment on**

**Purpose:** Make predictions on news articles based on title and subtitles

**3. Calculate final sentiment values**

**Purpose:** Calculate the final sentiment score for all the predicted data points, and combine them with annotated data point to a csv file, that will function as the input for visualization

-----------------------------------------------------------------------------------------------------------------------

### <u>Visualization Module:</u>

**1. Build combined indicator datafile for visualization **

**Purpose:** To extract relevant values from indicator data files and combine into one csv file with a single column for each of the indicator values. Assume that individual indicator data files are contained within `better_dwelling_capstone/visualization/data/financial_indicator_data/`. Output file will be created in `visualization/data/`

**2. Run final visualization **

**Purpose:** To visualize the correlation between changes in news sentiment against trend in economic indicator over a period of time.

