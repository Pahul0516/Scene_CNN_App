import torch
from torchvision import models
import os


class Places365Model:
    def __init__(self):
        self.device = torch.device("cpu")
        self.model = self._load_model()
        self.categories = self._load_categories()

    def _load_model(self):
        model = models.resnet18(num_classes=365)
        weight_path = os.path.join(
            os.path.dirname(__file__),
            "../../resources/resnet18_places365.pth.tar"
        )

        checkpoint = torch.load(weight_path, map_location=self.device)
        state_dict = {
            str.replace(k, "module.", ""): v
            for k, v in checkpoint["state_dict"].items()
        }

        model.load_state_dict(state_dict)
        model.eval()
        return model

    def _load_categories(self):
        cat_path = os.path.join(
            os.path.dirname(__file__),
            "../../resources/categories_places365.txt"
        )

        with open(cat_path) as f:
            categories = [line.strip().split(" ")[0][3:] for line in f]

        return categories
