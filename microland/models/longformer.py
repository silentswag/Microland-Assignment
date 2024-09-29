"""from transformers import LongformerTokenizer, LongformerModel
import torch

LONGFORMER_MODEL_NAME = "allenai/longformer-base-4096"

model = LongformerModel.from_pretrained(LONGFORMER_MODEL_NAME)
tokenizer = LongformerTokenizer.from_pretrained(LONGFORMER_MODEL_NAME)

def process(text):
    # Encode the input text
    inputs = tokenizer.encode(text, return_tensors="pt", max_length=4096, truncation=True)
    
    # Get the model output
    output = model(inputs)
    
    # Extract the last hidden state of the first token (typically the [CLS] token)
    cls_embedding = output.last_hidden_state[0][0]  # Shape: (hidden_size,)
    
    # Convert the embedding to a NumPy array and then to a string
    cls_embedding_str = ', '.join(map(str, cls_embedding.tolist()))
    
    return cls_embedding_str
"""