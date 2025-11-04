# OneHitKill-itchio-bot

## Introduction

One Hit Kill is a game itch.io website, where you have to fight off endless enemies while you health is at 1HP. Kill them in one hit

Each enemies have their own weakness.
- press (WASD) to choose element
- press Arrow keys to choose attack stance

This is a bot to automate that game with pytorch.

![alt text](img_for_readme/introduction/image1.png)
![alt text](img_for_readme/introduction/image2.png)

You can try the game out yourself here: https://adamvian.itch.io/one-hit-kill


## Setup instructions to run train system locally
You can skip to step 4 if you want to run without training, as there might be .pth (aka weight files) already upon cloning this repository

### step 1 - screen record (or data collection)

go to "01 records" folder and run `recorder.py` script, to start collecting images

### step 2 - data labelling (folder-based labels)

go to "02 labelling" folder and run `generate_dataset_folder.py` script, to generate format dataset as follows.
```
(inside "datasets/" folder)

dataset_{time_stamp}/
├── class1/
│   ├── image1.png
│   ├── image2.png
│   └── ...
├── class2/
│   ├── image1.png
│   └── ...
```
Once that, you start manually **move** images from screenshots folder in "01 records" to dataset folder in "02 labelling" with a matching category

### step 3 - train model
go to "03 train" folder and move dataset to "data_to_use" folder
and edit inside `trainer.ipynb`
```
dataset = datasets.ImageFolder(
    root=os.path.join("data_to_use", {YOUR_DATASET_FOLDER_NAME}),
    transform=transform
)
```
run the whole notebook to obtain weight file

and move "simplecnn_weights.pth" to "04 utilize" folder

### step 4 - use model to run bot to play game for us
finally go to "04 utilize" folder, and run `bot.py` script to let the bot play your game!




## Model's performance & architecture
```
----------------------------------------------------------------
        Layer (type)               Output Shape         Param #
================================================================
            Conv2d-1         [-1, 16, 128, 128]             448
         MaxPool2d-2           [-1, 16, 64, 64]               0
            Conv2d-3           [-1, 32, 64, 64]           4,640
         MaxPool2d-4           [-1, 32, 32, 32]               0
            Conv2d-5           [-1, 64, 32, 32]          18,496
         MaxPool2d-6           [-1, 64, 16, 16]               0
            Linear-7                  [-1, 128]       2,097,280
           Dropout-8                  [-1, 128]               0
            Linear-9                   [-1, 26]           3,354
================================================================
Total params: 2,124,218
Trainable params: 2,124,218
Non-trainable params: 0
----------------------------------------------------------------
Input size (MB): 0.19
Forward/backward pass size (MB): 4.38
Params size (MB): 8.10
Estimated Total Size (MB): 12.67
----------------------------------------------------------------
```
provided weight in repository for model, only make model have accuracy at 52.71%. Still needs further improvement