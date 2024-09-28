from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModelForQuestionAnswering.from_pretrained("bert-base-uncased")

def generate_answers(question:str, context:str):
    if isinstance(context, torch.Tensor):
        # Convert tensor to a string, if it's a single element tensor
        if context.numel() == 1:
            context = str(context.item())
        else:
            # If it's a tensor with multiple elements, convert to list of strings
            context = " ".join(map(str, context.tolist()))
    elif isinstance(context, list):
        # If context is a list, join it into a single string
        context = " ".join(context)
    elif not isinstance(context, str):
        raise ValueError("Context must be a string, tensor, or list of strings")
        # Tokenize and encode the inputs correctly
    inputs = tokenizer.encode_plus(
        question, 
        context, 
        return_tensors="pt", 
        max_length=512, 
        truncation=True
    )
    input_ids = inputs["input_ids"].tolist()[0]

    # Get model outputs
    outputs = model(**inputs)
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    # Get the most likely start and end of the answer
    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores) + 1

    # Decode the tokens back to the answer string
    answer = tokenizer.convert_tokens_to_string(
        tokenizer.convert_ids_to_tokens(input_ids[start_index:end_index])
    )
