import glob
import pandas as pd
import os


def write_emodb_csv(emotions=['angry', 'sad', 'neutral', 'fear', 'happy'], train_name="train_emo.csv",
                    test_name="test_emo.csv", train_size=0.8, verbose=1):
    """
    Reads speech emodb dataset from directory and write it to a metadata CSV file.
    params:
        emotions (list): list of emotions to read from the folder, default is ['sad', 'neutral', 'happy']
        train_name (str): the output csv filename for training data, default is 'train_emo.csv'
        test_name (str): the output csv filename for testing data, default is 'test_emo.csv'
        train_size (float): the ratio of splitting training data, default is 0.8 (80% Training data and 20% testing data)
        verbose (int/bool): verbositiy level, 0 for silence, 1 for info, default is 1
    """
    target = {"path": [], "emotion": []}
    categories = {
        "W": "angry",
        "L": "boredom",
        "E": "disgust",
        "A": "fear",
        "F": "happy",
        "T": "sad",
        "N": "neutral"
    }
    # delete not specified emotions
    categories_reversed = { v: k for k, v in categories.items() }
    for emotion, code in categories_reversed.items():
        if emotion not in emotions:
            del categories[code]
    for file in glob.glob("data/emodb/wav/*.wav"):
        try:
            emotion = categories[os.path.basename(file)[5]]
        except KeyError:
            continue
        target['emotion'].append(emotion)
        target['path'].append(file)
    if verbose:
        print("[EMO-DB] Total files to write:", len(target['path']))
        
    # dividing training/testing sets
    n_samples = len(target['path'])
    test_size = int((1-train_size) * n_samples)
    train_size = int(train_size * n_samples)
    if verbose:
        print("[EMO-DB] Training samples:", train_size)
        print("[EMO-DB] Testing samples:", test_size)   
    X_train = target['path'][:train_size]
    X_test = target['path'][train_size:]
    y_train = target['emotion'][:train_size]
    y_test = target['emotion'][train_size:]
    pd.DataFrame({"path": X_train, "emotion": y_train}).to_csv(train_name)
    pd.DataFrame({"path": X_test, "emotion": y_test}).to_csv(test_name)


def write_tess_ravdess_csv(emotions=['angry', 'sad', 'neutral', 'fear', 'happy'], train_name="train_tess_ravdess.csv",
                            test_name="test_tess_ravdess.csv", verbose=1):
    train_target = {"path": [], "emotion": []}
    test_target = {"path": [], "emotion": []}
    
    for category in emotions:
        # for training speech directory
        total_files = glob.glob(f"data/training/Actor_*/*_{category}.wav")
        for i, path in enumerate(total_files):
            train_target["path"].append(path)
            train_target["emotion"].append(category)
        if verbose and total_files:
            print(f"[TESS&RAVDESS] There are {len(total_files)} training audio files for category:{category}")
    
        # for validation speech directory
        total_files = glob.glob(f"data/validation/Actor_*/*_{category}.wav")
        for i, path in enumerate(total_files):
            test_target["path"].append(path)
            test_target["emotion"].append(category)
        if verbose and total_files:
            print(f"[TESS&RAVDESS] There are {len(total_files)} testing audio files for category:{category}")
    pd.DataFrame(test_target).to_csv(test_name)
    pd.DataFrame(train_target).to_csv(train_name)


def write_custom_csv(emotions=['angry', 'sad', 'neutral', 'fear', 'happy'], train_name="train_custom.csv", test_name="test_custom.csv",
                    verbose=1):
    """
    Reads Custom Audio data from data/*-custom and then writes description files (csv)
    params:
        emotions (list): list of emotions to read from the folder, default is ['sad', 'neutral', 'happy']
        train_name (str): the output csv filename for training data, default is 'train_custom.csv'
        test_name (str): the output csv filename for testing data, default is 'test_custom.csv'
        verbose (int/bool): verbositiy level, 0 for silence, 1 for info, default is 1
    """
    train_target = {"path": [], "emotion": []}
    test_target = {"path": [], "emotion": []}
    for category in emotions:
        # train data
        for i, file in enumerate(glob.glob(f"data/train-custom/*_{category}.wav")):
            train_target["path"].append(file)
            train_target["emotion"].append(category)
        if verbose:
            try:
                print(f"[Custom Dataset] There are {i} training audio files for category:{category}")
            except NameError:
                # in case {i} doesn't exist
                pass
        
        # test data
        for i, file in enumerate(glob.glob(f"data/test-custom/*_{category}.wav")):
            test_target["path"].append(file)
            test_target["emotion"].append(category)
        if verbose:
            try:
                print(f"[Custom Dataset] There are {i} testing audio files for category:{category}")
            except NameError:
                pass
    
    # write CSVs
    if train_target["path"]:
        pd.DataFrame(train_target).to_csv(train_name)

    if test_target["path"]:
        pd.DataFrame(test_target).to_csv(test_name)

def write_surrey_csv(emotions=['angry', 'sad', 'neutral', 'fear', 'happy'], train_name="train_surrey.csv",
                    test_name="test_surrey.csv", train_size=0.8, verbose=1):
    
    
    # target = {"path": [], "emotion": []}
    categories = {
        "a": "angry",
        "f": "fear",
        "h": "happy",
        "sa": "sad",
        "n": "neutral",
    }
    target = {"path": [], "emotion": []}
    
    for file in glob.glob('data/surrey/*.wav'):
        try:
            part = os.path.basename(file).split('_')[1]
            if part.startswith("a"):
                emotion = "a"
                target['emotion'].append(categories[emotion])
                target['path'].append(file)
            elif part.startswith("f"):
                emotion = "f"
                target['emotion'].append(categories[emotion])
                target['path'].append(file)
            elif part.startswith("h"):
                emotion = "h"
                target['emotion'].append(categories[emotion])
                target['path'].append(file)
            elif part.startswith("sa"):
                emotion = "sa"
                target['emotion'].append(categories[emotion])
                target['path'].append(file)
            elif part.startswith("n"):
                emotion = "n"
                target['emotion'].append(categories[emotion])
                target['path'].append(file)
        except KeyError:
            continue

    if verbose:
        print("[surrey] Total files to write:", len(target['path']))
        
    # dividing training/testing sets
    n_samples = len(target['path'])
    test_size = int((1-train_size) * n_samples)
    train_size = int(train_size * n_samples)
    if verbose:
        print("[surrey] Training samples:", train_size)
        print("[surrey] Testing samples:", test_size)   
    X_train = target['path'][:train_size]
    X_test = target['path'][train_size:]
    y_train = target['emotion'][:train_size]
    y_test = target['emotion'][train_size:]
    pd.DataFrame({"path": X_train, "emotion": y_train}).to_csv(train_name)
    pd.DataFrame({"path": X_test, "emotion": y_test}).to_csv(test_name)

# def write_crema_csv(emotions=['angry', 'sad', 'neutral', 'fear', 'happy'], train_name="train_crema.csv",
#                     test_name="test_crema.csv", train_size=0.8, verbose=1):
    
#     target = {"path": [], "emotion": []}
    
    
#     for file in glob.glob('data/crema/*.wav'):
#         try:
#             part = os.path.basename(file).split('_')[2]
#             if part == 'SAD':
#                 target['emotion'].append('sad')
#                 target['path'].append(file)
#             elif part == 'ANG':
#                 target['emotion'].append('angry')
#                 target['path'].append(file)
#             elif part == 'FEA':
#                 target['emotion'].append('fear')
#                 target['path'].append(file)
#             elif part == 'HAP':
#                 target['emotion'].append('happy')
#                 target['path'].append(file)
#             elif part == 'NEU':
#                 target['emotion'].append('neutral')
#                 target['path'].append(file)
#         except KeyError:
#             continue
#     if verbose:
#         print("[Crema] Total files to write:", len(target['path']))
        
#     # dividing training/testing sets
#     n_samples = len(target['path'])
#     test_size = int((1-train_size) * n_samples)
#     train_size = int(train_size * n_samples)
#     if verbose:
#         print("[Crema] Training samples:", train_size)
#         print("[Crema] Testing samples:", test_size)   
#     X_train = target['path'][:train_size]
#     X_test = target['path'][train_size:]
#     y_train = target['emotion'][:train_size]
#     y_test = target['emotion'][train_size:]
#     pd.DataFrame({"path": X_train, "emotion": y_train}).to_csv(train_name)
#     pd.DataFrame({"path": X_test, "emotion": y_test}).to_csv(test_name)