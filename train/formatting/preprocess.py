import json
import re
import random
from tqdm import trange, tqdm

data={"train":[], "valid":[]}

additive=[]
extra=[]
with open("inp.txt") as f:
    d = f.readlines()
    additive+=d

with open("out.txt") as f:
    d=f.readlines()
    additive+=d[:100000]
    extra+=d[100000:]

print(len(additive))
print(len(extra))
discarded=0

processed=[]
processed_ext=[]
pbar = tqdm(total=len(processed))
pbar.set_description("Preprocessing")
for sentence in additive:
    sentence = sentence.lower().strip()
    # creating a space between a word and the punctuation following it
    # eg: "he is a boy." => "he is a boy ."
    sentence = re.sub(r"([?.!,])", r" \1 ", sentence)
    sentence = re.sub(r'[" "]+', " ", sentence)
    # replacing everything with nothing except (a-z, A-Z, 0-9 ".", "?", "!", ",", "'", " ", "/", "%", "#")
    sentence = re.sub(r"[^a-zA-Z0-9?.!,\'\s]+", "", sentence)
    # getting rid of extra spaces
    sentence = re.sub(r"(\s+){2,}", " ", sentence)
    sentence = sentence.strip()
    if len(sentence) <= 100:
      processed.append(sentence)
    else:
      discarded+=1
    pbar.update(1)
pbar.close()

pbar = tqdm(total=len(processed_ext))
pbar.set_description("Preprocessing extras")
for sentence in extra:
    sentence = sentence.lower().strip()
    # creating a space between a word and the punctuation following it
    # eg: "he is a boy." => "he is a boy ."
    sentence = re.sub(r"([?.!,])", r" \1 ", sentence)
    sentence = re.sub(r'[" "]+', " ", sentence)
    # replacing everything with nothing except (a-z, A-Z, 0-9 ".", "?", "!", ",", "'", " ", "/", "%", "#")
    sentence = re.sub(r"[^a-zA-Z0-9?.!,\'\s]+", "", sentence)
    # getting rid of extra spaces
    sentence = re.sub(r"(\s+){2,}", " ", sentence)
    sentence = sentence.strip()
    if len(sentence) <= 100:
      processed_ext.append(sentence)
    else:
      discarded+=1
    pbar.update(1)
pbar.close()
del additive
del extra

print("\ndiscarded ", discarded, "entries")

for partition in trange(0,len(processed)-1600,80):
  template={"personality":["jade"], "utterances":[]}
  for i in range(partition, partition+80,2):
    canvas= {"candidates":[], "history":[]}
    for p in range(9):
        canvas["candidates"].append(processed_ext[random.randint(0,len(processed_ext)-1)])
    canvas["candidates"].append(processed[i+1])
    st = (i-9)
    if st < 0:
      st=0
    canvas["history"]=processed[st:i+1]
    template["utterances"].append(canvas)
  data["train"].append(template)

for part in trange(len(processed)-1600,len(processed)-81,80):
  template={"personality":["jade"], "utterances":[]}
  for i in range(part, part+80, 2):
    canvas= {"candidates":[], "history":[]}
    for p in range(1):
        canvas["candidates"].append(processed[random.randint(0,len(processed)-1)])
    for p in range(8):
        canvas["candidates"].append(processed_ext[random.randint(0,len(processed_ext)-1)])
    canvas["candidates"].append(processed[i+1])
    st = (i-9)
    if st < 0:
      st=0
    canvas["history"]=processed[st:i+1]
    template["utterances"].append(canvas)
  data["valid"].append(template)

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)