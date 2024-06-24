# PubMed Article Summarizer

## Table of Contents

1. Repository
   - Getting Started
2. Data Exploration and Preparation
   - Explore the dataset to understand its structure and contents
   - Preprocess the dataset to clean and prepare the text for summarization
3. Web Application Development
   - Web application using Flask
4. Generative AI Model Integration
   - T5 (Hugging Face) for text summarization

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Getting Started
This project aims to summarize PubMed articles using a fine-tuned text summarization model. The summarizer is deployed as a web application built with Flask.

### Directory Structure

```plaintext
web_app/
│
├── app.py
├── Preprocessing and Model.ipynb
├── requirements.txt
├── fine_tuned_model_final/
│   └── model.safetensors
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── README.md
```

### Running the App

Clone the Repository 
```shell
git clone https://github.com/ali0887/PubMed.git
```
You can also download the reporsitory as a zip file and unzip it in a seperate folder.

#### Set up a virtual Environment and run the requirements.txt file
```shell
pip install -r requirements.txt
```
#### Run the Python app to run the application

## Data Exploration and Preparation

### Explore the dataset to understand its structure and contents
- After loading up the Data and going throught both the article and abstract columns, it was visible that the data was already pretty straightforward to work with.
- On lookup for the type of data, we found that the summaries provided for the articles averaged at 300 words whereas the articles averaged at 4000.
- Furthermore the length of articles were of varying ranges from below hundred to well above 100,000.

### Preprocess the dataset to clean and prepare the text for summarization
#### Data Cleaning
- Data contained unnecessary references to figures that were not available hence these were removed.
- References in Square Brackets e.g. [ 11, 12 ] provided no context at all and hence these were removed.
- Common data cleaning practices such as extra whitespaces or newline characters were removed.
- AlphaNumeric characters were not removed since they contained important information that could be used by the model to better summarize the text.

#### Stop words and Lemmantization
- Common stopwords were removed from the dataset to avoid unnecessary training.
- Lammentization was used to revert the words back to their base meaning to assist in model understanding of the text.

#### Tokenization
- After the data has been cleaned and preprocessed, we converted each article into its respective tokens to be used for training and evaluation by the model.
- Articles were padded and truncated to a maximum length to maintain consistency and manage memory efficiently during training.

-With these preprocessing steps, the dataset is now ready for effective training and evaluation, ensuring that the model can focus on the most relevant and clean information for summarization.


## Web Application Development

-To develop the Web Application and link the model with the web interface, we used Flask for its simplicity and ease of access.
-The application allows users to input PubMed articles and provides a summarized version of the text using the fine-tuned model.
-The application also allows you to choose between bried and detailed summary of the article.

### Web Page
- The Web Page is made in HTML, CSS, and Javascript.
- It follows a simplistic design to allow the users to input their articles and get the output summary back.

### Flask
- Links the model and the web page together to provide a seemless experience.
- Main Tasks include:
   1. Loading up the saved model and tokenizer.
   2. Establishing a link between the web page to GET and POST.
   3. When input comes, preprocessing the data and setting the appropriate parameters for the model.
   4. Running the model and sending the results back to the web page.
      

## Generative AI Model Integration

The choice for choosing the T5 (Text to Text Transfer Transformer) for the generative AI Model came simply down to a selection between the multiple models available and sticking to it.
-The T5 Model offers multiple different models to choose from. For this project, the model choosen was the t5-small model due to the hardware and time constraints on the project.

Having ran the model with varying train data size, processed and unprocessed data, there are many inferences that can be made.
1. Cleaning the Dataset improves the metrics, performance and the time taken to fine tune the model.
2. Fine Tuning the model with a quarter of the original training samples reduces the training time but also reduces the quality of the model.
3. Without preprocessing the data, the summarized text produced contains text that do nnot corelate with the article at all.

The Tuning was done on Kaggle using the accelerator: GPU T4 x 2 that provided 2 GPU's with 15 GB of memory each alongside 4 cores and 29 GB of system RAM.

For calculating the performance of the model, we used the ROGUE Metric specifically the ROGUE 1, ROGUE 2, and ROGUE L respectively.

The Model being used limited us to a maximum token of 512 which is approximately 628 english words

The Fine Tuning was done with the following specifications:
   1. Epochs = 3
   2. Batch Size = 8
   3. Learning Rate = 0.0001

For a total training time of 3 Hours we got the following results:
   1. Rogue 1: 0.50900
   2. Rogue 2: 0.21800
   3. Rogue L: 0.44250

- The rogue scores we obtained show us that the model understands our dataset well enough. The performance is neither absolutely bad nor absolutely amazing. it strikes in between the two providing good summaries.
- Another run of the Model with a smaller training dataset but greater epoch run showed that the model started to perform significantly worse after finishing the 3rd Epoch. As such the Final Model only trains upto 3 epochs.
- As far as betterment of the application is concerned, it could be improved by using techniques like ensemble, better fine tuning, or more effecient pre processing of the data however, was not possible due to the time constraint.
