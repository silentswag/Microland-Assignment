from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")
model = AutoModelForQuestionAnswering.from_pretrained("distilbert-base-uncased-distilled-squad")

def generate_answers(question, context):
    # Encode the inputs
    inputs = tokenizer.encode_plus(question, context, return_tensors="pt", max_length=512, truncation=True)
    input_ids = inputs["input_ids"].tolist()[0]

    # Get model outputs
    outputs = model(**inputs)
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    # Get the most likely start and end of the answer
    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores) + 1

    # Decode the answer
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[start_index:end_index]))
    return answer

