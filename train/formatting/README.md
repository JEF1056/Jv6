# Data Formatting
## Preprocessor
This repo includes a file to preprocess your data. Unfortunately it is ~~extra spaghetti code~~, but decently usable.

### Code usage details
----------------------------
The data I used for train data can be found [here](https://www.kaggle.com/jef1056/anime-subtitles) Unfortunately, the discord (validation) data used was from various servers, and I was asked not to release it.
#### Assumptions
1. Your text file(s) are assumed to be person to person conversation, with line 1 being the first person and line 2 being the second person. 
2. Lines end with `\n`.
3. There is only one personality to follow.
4. You have a validation set & a training set, in seperate text files.

#### Instructions
In `avg_length.py`:
1. Change the file read in line `2` to each of your 2 text files
2. Estimate the average length and standard devation of sentences in your dataset. Try and normalize the data. A generally good formula is `(Average + Standard Deviation) + 5`

In `preprocess.py`:

1. On lines `38` and `58` change the max length you found before from `avg_length.py`
2. On lines `70` adn `84` change the personality to use, unless you're ok with `jade` being the personality
3. On lines `10` and `14`, manually modify the text files to read from.
    - `inp.txt` contains input data that the bot should attempt to mimic (your goal personalitites)
    - `out.txt` is the validation data. Preferrably, it comes from the audience the chatbot will be interacting with. Some of this data will e included in the training set.
4. On lines `16-17`, change the number of lines to read.

----------------------------
## Format details
- Each entry is a dict with two keys personality and utterances, the dataset is a list of entries. In each entry, there is a
    - personality:  list of strings containing the personality of the agent. This data is not interpreted, and serves primarily as a "marker". As such, multiple of the same key can be trained on to improve the overall model.
    - utterances: list of dictionaries, each of which has two keys which are lists of strings.
        1. candidates: [next_utterance_candidate_1, ..., next_utterance_candidate_19]
        The last candidate is the ground truth response observed in the conversational data
        2. history: [dialog_turn_0, ... dialog_turn N], where N is an odd number since the other user starts every conversation.
- Preprocessing:
    - Spaces before periods/punctuation at end of sentences
    - Everything lowercase
    - All data should be `a-z, A-Z, 0-9 ".", "?", "!", ",", "'", " ", "/", "%", "#"`
- Keep the validation set small!! the training script will go through all the validation samples before saving the model.