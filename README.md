# Schizophrenia Patient Data Analysis


## Run App
- Go to the app folder
```
cd streamlit-app
```
- Set OPENAI API Key
  
  Export OPENAI_API_KEY in the VM
  
  Set api_key_string in Prototype.py
  
- Run the Prototype
```
nohup python3 Prototype.py &
tail -f nohup.out
```
- View the App
  Use the localhost or IP Address assigned to the VM. For example, the below URL can be accessed by anyone. This Demo VM is VM is running in Azure.
```
http://13.83.89.195:8080
Login: 
     user: admin 
     password: Admin@123
```

## Project Components 
### Emotion Detection from Speech
- it can be tested indepdentely as follows
```
cd emotion-detection
pip install -r requirements.txt
python3 main.py
```
### Emotion Detection from Video (Facial Expression)


## ToDo
- Use relative path for images.
- At this point, users who will clone this repo, need to change the image file path in streamlit-app/Prototype.py based on the local folder location.


## Reference Resources
### Behavior Detection:

https://github.com/ShoupingShan/Abnormal-behavior-Detection 

### Index the results and allow the Lab users search the results

https://github.com/Azure/azureml-examples/tree/main/sdk/python/generative-ai/rag/notebooks

### Text Classification using Azure AI

https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/system/inference/text-classification/entailment-contradiction-batch.ipynb

### Using Huggingface Model

https://github.com/balakreshnan/Samples2021/blob/main/AzureML/hugginface1.md

### Sentiment Analysis

https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/system/evaluation/text-classification/sentiment-analysis.ipynb
https://github.com/easonlai/analyze_customer_reviews_with_aoai/blob/main/analyze_customer_reviews_with_aoai.ipynb
https://medium.com/@lokaregns/effortless-sentiment-analysis-with-hugging-face-transformers-a-beginners-guide-359b0c8a1787

### Ethical AI
https://go.microsoft.com/fwlink/p/?linkid=2235870

### Implement RAG 
https://github.com/Azure/azureml-examples/tree/main/sdk/python/generative-ai/rag/notebooks

### Prompt Flow
https://github.com/Azure/azureml-examples/tree/main/sdk/python/generative-ai/promptflow

### Multi-Modal Object Tracking
https://github.com/Azure/azureml-examples/tree/main/cli/foundation-models/system/inference/video-multi-object-tracking


