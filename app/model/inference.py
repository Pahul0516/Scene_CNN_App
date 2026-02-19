import torch
from torchvision import transforms
from ..utils.image_utils import load_image_from_bytes
from .model_loader import Places365Model


class SceneClassifier:
    def __init__(self):
        self.model_wrapper = Places365Model()
        self.model = self.model_wrapper.model
        self.categories = self.model_wrapper.categories

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def predict_from_bytes(self, image_bytes: bytes):
        image = load_image_from_bytes(image_bytes)
        tensor = self.transform(image).unsqueeze(0)

        with torch.no_grad():
            output = self.model(tensor)
            probs = torch.nn.functional.softmax(output, dim=1)
            top_idx = probs.argmax().item()

        return self.categories[top_idx]