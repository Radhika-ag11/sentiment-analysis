from transformers import pipeline
classifier = pipeline('sentiment-analysis')

x="i am good in crime"
results = classifier([x])
for result in results:
    print(f"label: {result['label']}, with score: {round(result['score'], 4)}")