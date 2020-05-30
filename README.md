# Jade AI (V6)
### What is Jade? 
Jade is a contextual chatbot, using OpenAI's GPT-2 transformer model to generate logical conversation. I wrote a more detailed description of Jade's capabilities (with screenshots!!) [here](https://dev.to/jef1056/jade-ai-549i).

----------------------------
## Usage
### To deploy, it's rather simple.
#### Requirements
- Python 3+
- Pip 3
- 1 vCPU (more cores doesn't matter, but high single-core preformance does)
- 1.25GB or more of RAM
- ~10GB of storage
#### Instructions
1. Download the [pretrained model](haha-i-havent-uploaded-it-yet) or [train your own](#train)
2. Run `pip3 install -r reqirements.txt` in this folder
3. Create a `config.json` file based on `config_example.json`
4. run `interact.py`

### Here is a table of commands for `interact.py` (in discord)
Prefix is `JD`
|    Command    |   Short Explanation  | Usage Example |
|---------------|:----------------:|:-------------:|
| JD -h |  Help menu | `JDT -h` |
| JD -p | Ping menu | `JDT -p` |
| JD -v |  Voting menu | `JDT -v` |
| JD -s | Settings menu | `JDT -s` or `JDT -s [setting] [new value]` |
| JD -r | Resetting history or settings | `JDT -r` or `JDT -r [history or settings]` |
| JD [message] | Talk to Jade! | `JDT [message]` |

### Here is a table of arguments for `interact.py`
Argument | Type | Default value | Description
---------|------|---------------|------------
model | `str` | `"openai-gpt"` | Path, url or short name of the model
max_history | `int` | `4` | Number of previous utterances to keep in history
device | `str` | `cuda` if `torch.cuda.is_available()` else `cpu` | Device (cuda or cpu)
no_sample | action `store_true` | Set to use greedy decoding instead of sampling
max_length | `int` | `20` | Maximum length of the output utterances
min_length | `int` | `1` | Minimum length of the output utterances
seed | `int` | `0` | Seed
temperature | `int` | `0.7` | Sampling softmax temperature
top_k | `int` | `0` | Filter top-k tokens before sampling (`<=0`: no filtering)
top_p | `float` | `0.9` | Nucleus filtering (top-p) before sampling (`<=0.0`: no filtering)
f | `idk...` | `N/A` | Colab is weird ok

##### All of these (except for the server settings) are availabe for user modifications via the `JD -s`  command.
<a name="train"></a>

## Training
### Training is a bit more difficult.
#### Requirements

- Python 3+
- Pip 3
- (Preferred) a server with GPU functionality. (Multi-GPU setups are supported!)
  - A single Tesla T4 will take ~12 hours to finetune the model, wouthout FP16. The formatted dataset size was ~400mb. See the dataset format [here](train/formatting/example_data.json)
  - FP16 will reduce the vram usage and increase the speed of the model training. Depending on your hardware configuration, your results may vary.
- (Preffered) 25 + GB of ram
  - <span style="color:red">WARNING!!</span> Large datasets (> 200 mb formatted datasets) may require mare than 25GB of ram during tokenization.
  - The pretrained model took ~45GB of ram to train
- (Reccomended) 30gb of storage

#### Instructions
See the [README.md](train/README.md) in the train folder to see all the possible arguments for thr training script.

```bash
python3 train.py --dataset_path data.json --model gpt2 --gradient_accumulation_steps=4 \
--lm_coef=2.0 --fp16=O1 --max_history=4 --n_epochs=1 --num_candidates=0 \
--personality_permutations=2 --train_batch_size=4 --valid_batch_size=4
```

1. Run `pip3 install -r reqirements-train.txt` in this folder
2. Use the [formatter](train/formatting/README.md) to create the dataset in the correct format.
3. Run the command above (which will replicate my results), or add `-m torch.distributed.launch --nproc_per_node=8` after python if you're using more than one GPU.
   - If the progam is crashing with no errors during padding, use `htop` to check your RAM usage. Most cloud solutions will allow you to edit the machine memory size, or you can add swap.
4. Use [nvtop](https://github.com/Syllo/nvtop) or `nvidia-smi` to monitor GPU usage after tokenization.
   - Use FP16 if vram usage is really high
   - try to max out your GPU(s) by increasing or decreasing `--train_batch_size=4 --valid_batch_size=4`. A Tesla T4 will not be maxed out until it receives batches of 4.
5. Complete training.
   - <span style="color:red">WARNING!!</span> TRAINING IS NOT DONE UNTIL ALL VALIDATION IS COMPLETE. Try and keep the validation set small.
   - The model will be saved to `runs/[DATE]`

#### Post-Training
There's a bit more to make the completed model compatable with `interact.py`.
Unfortunately, I need to re-code this part, but I'll have it uploaded soon!

(if you want to do it yourself)
1. read the tokenizer file and use it to tokenize the personalities in your detaset file
2. save the tokenized personalities in a list
3. use pickle to save the list to `versions.p` in the model folder