import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
import joblib
from pathlib import Path
from pre_processing import preprocess

MODEL_NAME = "indolem/indobertweet-base-uncased"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class IndoBERTweetBiGRU(nn.Module):

    def __init__(
        self,
        bert_model="indolem/indobertweet-base-uncased",
        hidden_size=128,
        num_classes=5,
        dropout=0.3
    ):

        super(IndoBERTweetBiGRU, self).__init__()

        # IndoBERTweet
        self.bert = AutoModel.from_pretrained(
            bert_model
        )

        # BiGRU
        self.bigru = nn.GRU(
            input_size=768,
            hidden_size=hidden_size,
            batch_first=True,
            bidirectional=True
        )

        # Dropout
        self.dropout = nn.Dropout(dropout)

        # Fully Connected
        self.fc = nn.Linear(
            hidden_size * 2,
            num_classes
        )

    def forward(
        self,
        input_ids,
        attention_mask
    ):

        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        sequence_output = outputs.last_hidden_state

        gru_output, hidden = self.bigru(
            sequence_output
        )

        forward_hidden = hidden[-2]

        backward_hidden = hidden[-1]

        hidden_concat = torch.cat(
            (forward_hidden, backward_hidden),
            dim=1
        )

        x = self.dropout(hidden_concat)

        logits = self.fc(x)

        return logits

#path
BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "model_fl_e3_2e5.pth"
LABEL_ENCODER_PATH = BASE_DIR / "models" / "label_encoder.pkl"

# tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# model
model = IndoBERTweetBiGRU()

model.load_state_dict(torch.load(MODEL_PATH, map_location=device))

model.to(device)
model.eval()

# label encoder
label_encoder = joblib.load(LABEL_ENCODER_PATH)

LABEL_MAPPING = {
    "Kata Kasar dan Vulgar": "Rude Words",
    "Body Shaming": "Body Shaming",
    "Hate Speech": "Hate Speech",
    "Non-Cyberbullying": "Non-Cyberbullying"
}

def predict_text(text):
    text = preprocess(text)
    
    encoding = tokenizer(
        text,
        truncation=True,
        padding=True,
        max_length=128,
        return_tensors="pt"
    )

    input_ids = encoding["input_ids"].to(device)
    attention_mask = encoding["attention_mask"].to(device)

    with torch.no_grad():
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        probs = torch.softmax(outputs, dim=1)

        pred = torch.argmax(probs, dim=1).item()

    label = label_encoder.inverse_transform([pred])[0]
    display_label = LABEL_MAPPING.get(label, label)

    return {
        "label": display_label,
        "probability": probs[0].tolist()
    }