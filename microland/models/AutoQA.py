from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering
import torch
model_name="distilbert-base-uncased-distilled-squad"
#loading tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
qa_model = pipeline("question-answering",model=model, tokenizer=tokenizer)

def generate_answers(question:str, context:str)-> str:
    if not isinstance(question, str):
        raise ValueError(f"Expected `question` to be a string, got {type(question)} instead.")
    if not isinstance(context, str):
        raise ValueError(f"Expected `context` to be a string, got {type(context)} instead.")
        
    inputs = tokenizer.encode_plus(
        question, 
        context, 
        return_tensors="pt", 
        max_length=512, 
        truncation=True
    )
    input_ids = inputs["input_ids"].tolist()[0]

    #model outputs
    outputs = model(**inputs)
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores) + 1

    if start_index >= end_index or start_index < 0 or end_index > len(input_ids):
        return "Answer not found or index out of range."
    answer = tokenizer.convert_tokens_to_string(
        tokenizer.convert_ids_to_tokens(input_ids[start_index:end_index])
    )
    return answer if answer else "No valid answer found."
