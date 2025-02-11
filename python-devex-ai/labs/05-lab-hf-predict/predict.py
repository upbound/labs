''' Prediction Text Generator Example: Use At Your Discretion '''
''' Upbound does not control the produced transformer content '''
from transformers import pipeline

print("loading model ...")
model=pipeline("text-generation", model="distilgpt2", truncation=False)

def predict(prompt):
    completion=model(prompt, pad_token_id=50256)[0]["generated_text"]
    return completion

while True:
    sentence_start=input("Which sentence start should be completed: ")
    if sentence_start == "quit":
        break
    answer=predict(sentence_start)
    print(answer.split(".")[0] + ".")
