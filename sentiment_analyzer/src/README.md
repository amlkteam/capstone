
`Employment_and_TSX_Two_stage_flair_training.ipynb`：ipython notebook that was used to train the models for employment and tsx datasets. 

`Load_and_predict.py`: This script is used to generate prediction results using trained models. User needs to download the model, and specify the directory of the model for predictio

`generate_senti_df.py`: This script is used to generate one sentiment score for each article. And combine annotated articles and predicted articles into one big dataframe `combined_sentiment_data.csv` for visualization

`undersampling_on_indicator_and_split.py`: the script used to undersample training data in the second stage of model fine-tuning.
