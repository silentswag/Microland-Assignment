from transformers import LongformerTokenizer, LongformerModel
LONGFORMER_MODEL_NAME = "allenai/longformer-base-4096"


model=LongformerModel.from_pretrained(LONGFORMER_MODEL_NAME)
tokenizer=LongformerTokenizer.from_pretrained(LONGFORMER_MODEL_NAME)

def process(text):
    inputs=tokenizer.encode(text,return_tensors="pt",max_length=4096,truncation=True)
    output=model(inputs)
    return output.last_hidden_state