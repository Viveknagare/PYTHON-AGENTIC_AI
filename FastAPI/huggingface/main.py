from transformers import pipeline

pipe = pipeline("image-text-to-text", model="google/gemma-3-4b-it")

messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"},
            {"type": "text", "text": "What animal is on the candy?"}
        ]
    },
]
pipe(text=messages)

# This code will install torch first and after that it will install the model locally which is upto 5gb and then next time whenever you run it will run locally in your machine and model will be running. Also dont forget initially to download the huggingface cli locally and also do the auth login and then it will download the model locally using the HF-cli