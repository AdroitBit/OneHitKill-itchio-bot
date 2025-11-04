import torch
import torch.nn as nn
import torch.nn.functional as F
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class SimpleCNN(nn.Module):
    """
    Simple 3-layer CNN for 128x128 RGB images.
    Automatically builds correct FC layer size.
    """

    def __init__(self, num_classes):
        super().__init__()

        # Input: (3, 128, 128)
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        # Output: (16, 128, 128)
        self.pool1 = nn.MaxPool2d(2, 2)
        # Output after pool1: (16, 64, 64)

        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        # Output: (32, 64, 64)
        self.pool2 = nn.MaxPool2d(2, 2)
        # Output after pool2: (32, 32, 32)

        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        # Output: (64, 32, 32)
        self.pool3 = nn.MaxPool2d(2, 2)
        # Output after pool3: (64, 16, 16)

        self.dropout = nn.Dropout(0.3)

        # Dynamically determine fc input size

        # ✅ Precompute FC input size (for 128x128 images)
        self.fc_input_size = 64 * 16 * 16
        self.fc1 = nn.Linear(self.fc_input_size, 128)
        self.fc2 = nn.Linear(128, num_classes)


    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool1(x)
        x = F.relu(self.conv2(x))
        x = self.pool2(x)
        x = F.relu(self.conv3(x))
        x = self.pool3(x)
        x = x.view(x.size(0), -1)
        x = self.dropout(F.relu(self.fc1(x)))
        x = self.fc2(x)
        return x
    
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleCNN(num_classes=26).to(device)
model.load_state_dict(torch.load("simplecnn_weights.pth", map_location=device))
model.eval()

model_classes = ['dark_center', 'dark_head', 'dark_none', 'dark_rock', 'dark_side', 'fire_center', 'fire_head', 'fire_none', 'fire_rock', 'fire_side', 'ice_center', 'ice_head', 'ice_none', 'ice_rock', 'ice_side', 'no_monster', 'none_center', 'none_head', 'none_none', 'none_rock', 'none_side', 'robot_center', 'robot_head', 'robot_none', 'robot_rock', 'robot_side']



import pyautogui
from PIL import Image
import torchvision.transforms as transforms
import time
import keyboard as kb


transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
])

attack_on_element_pattern={
    "robot": "a",
    "fire": "d",
    "ice": "s",
    "dark": "w",
    "none": "s",
}
attack_on_weakness_pattern={
    "none":"right",
    "side":"left",
    "head":"down",
    "center":"up",
    "rock":"right",
}


while True:
    time.sleep(1/10)
    # Capture screen region
    screenshot = pyautogui.screenshot()
    image = transform(screenshot).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)
    
    class_name = model_classes[predicted.item()]
    print("Detected:", class_name)

    if class_name=="no_monster":
        continue
    element, weakness = class_name.split("_")
    # print(element, weakness)
    for k, v in attack_on_element_pattern.items():
        if k == element:
            kb.press(v)
            time.sleep(0.05)
            kb.release(v)
            break

    for k, v in attack_on_weakness_pattern.items():
        if k == weakness:
            kb.press(v)
            time.sleep(0.05)
            kb.release(v)
            break
    
