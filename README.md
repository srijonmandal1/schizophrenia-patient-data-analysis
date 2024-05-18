# Schizophrenia Patient Data Analysis

## Goal
```
The primary goal is to develop a Schizophrenia Monitoring & Analysis System that leverages advanced AI technologies to assist medical professionals by providing a more standardized, objective, and efficient method of diagnosing and monitoring schizophrenic patients. 
This application will analyze multimodal data inputs - video recordings, speech patterns, and textual information from patient interactions to detect and predict symptom patterns and severity, aiding medical professionals in making informed treatment decisions.
```
## Problem Description

```
Schizophrenia is a complex and chronic mental health disorder marked by symptoms such as delusions, hallucinations, disorganized thinking and impaired social functioning, often co-occurs with depression, anxiety disorders, and substance abuse. 

The symptoms not only significantly impact individual’s functioning of daily life, but also pose a risk of harm to others.

Early intervention, comprehensive treatment approaches, and support from healthcare professionals, family, and community resources are essential in addressing the needs of individuals living with schizophrenia, but there is no existing effective solution.
```

## Solution Approach

### Functional Modules
![image info](./pictures/imagine_1.png)
#### Advanced AI Technologies are used for content synthesis and Q&A:
- OpenAI Prompt Engineering and Whisper: For processing and understanding natural language inputs and converting speech to text with high accuracy.
- Hugging Face Transformer and OpenAI for Emotion Detection: To interpret emotional states from text, providing insights into the patient's mental state.
- Emotion Detection from Video using YOLOv7 and PyTorch: To analyze facial expressions and body language from video data, offering another layer of emotional and symptomatic analysis. 

#### Data Visualization and Analysis:
- Data is presented using intuitive visualizations such as trend lines, scatter plots, and histograms, enabling clear tracking of progression or improvement over time. It is planned to automate insights and create charts using Gen-AI.

#### Application of AI for Prescriptive Analytics:
- ML Algorithms will be used to cluster the insights and predict certain behaviour and generate recommendations.

#### AI-driven Knowledge Management:
- Open-AI and RAG based Virtual Agent: It assists researchers and medical professionals by answering queries related to the patient data and broader schizophrenia research, facilitating an interactive, learning-enhanced environment.

### User Interaction

![image info](./pictures/imagine_2.png)

### App Execution

#### Run App
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

#### Project Components 
##### Emotion Detection from Speech
- it can be tested indepdentely as follows
```
cd emotion-detection
pip install -r requirements.txt
python3 main.py
```
##### Emotion Detection from Video (Facial Expression)

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


