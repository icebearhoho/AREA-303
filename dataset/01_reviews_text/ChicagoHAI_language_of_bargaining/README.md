---
license: cc-by-nc-sa-4.0
viewer: false
extra_gated_prompt: >-
  ### Language of Bargaining Data License Agreement
  
  All the data within this repo are under this [Data License Agreement](https://drive.google.com/file/d/1VXLYPIgd8rm6SoLXaH97KeDqwYmEmFc5/view?usp=share_link).
extra_gated_fields:
  First Name: text
  Last Name: text
  Email: text
  Affiliation: text
  Job Title: text
  By clicking Submit below I acknowledge that I have read the data license agreement, understand it, and agree to be bound by its terms and conditions: checkbox
extra_gated_button_content: Submit
---
# Language of Bargaining Dataset

## Dataset Description
- **Paper:** [https://arxiv.org/abs/2306.07117]()

## Dataset Summary

This repo contains the Natural Language (NL) and Alternating Offer (AO) negotation transcript data as described in https://aclanthology.org/2023.acl-long.735.pdf.

The data includes the "Bargaining Act" annotations for the NL setting.

## Dataset Information

Within the `negotiations-data.zip` compressed folder you will find two folders containing the AO and NL data.

### Alternating Offers (AO)

The AO data is found in the folder `ao`. The folder contains 230 files, each one representing a single negotation conducted in the AO setting. They are in JSONL format where each line adheres to the following schema:

```yaml
{
  "id": string,
  "role": string seller|buyer,
  "message": float,
  "created_at": datetime,
  "status": string
}
```

There are multiple ways you could load this data, here is an example using the [pandas Python package](https://pandas.pydata.org/) for loading a single negotiation transcript, e.g. `ao/299.jsonl`.
```
import pandas as pd

ao_file = 'ao/299.jsonl'
negotiation_df = pd.read_json(ao_file, orient='records', lines=True)
```

### Natural language (NL)

The NL data is found in the folder `nl`. The folder contains 178 files, each one representing a single negotation conducted in the NL setting. They are in JSON format and adhere to the following schema:

```yaml
{
  "duration_min": float,
  "turns": [
    [
      {
        "ID": string,
        "Role": string seller|buyer,
        "Word": string,
        "Span": string,
        "Spoken Numeric": string,
        "Numeric": string,
        "Category": string,
        "Firm or Soft": string,
        "External Incentive": string
      },
      ...
      {
        ...
      },
    ]
  ]
}
```

There are multiple ways you could load this data, here is an example using the json and [pandas Python package](https://pandas.pydata.org/) for loading a single negotiation transcript, e.g. `nl/100.json`.
```
import pandas as pd
import json

nl_file = 'nl/100.json'
with open(nl_file, 'r') as f:
  data = json.load(f)
  # data contains the data, in json, of the entire negotiation
for utt in data['turns']:
  turn_df = pd.DataFrame.from_records(utt)
  # turn_df contains a single utterance, as a dataframe, where each row corresponds to one transcribed word.
  # Process and do something with turn_df here...
```

### Annotation Instructions 

Below is a relevant portion of the instructions provided to annotators. It shoud help clarify the data:

- Span:
  - `x` on all tokens included in the actual offer
  - Be inclusive - main idea is to exclude entirely different sentences
- Spoken Numeric 
  - `t`:	if thousands place is spoken aloud (234,000), else blank
- Numeric (i.e. offer amount)
  - Single number (plain numeric, thousands)
    - 220
  - Range or Bounds
    - [220, 225] [,225] [220,]      
- Category
  - `n`:	Numeric Offer (common case) - used for new numeric offers (numbers that haven’t been mentioned yet)
  - `p`:	Push (request the other person move in my direction, mainly needs to reference offer made by other party)
  - `a`:	Allowance (offer to move in the other persons’ direction without explicit number, needs to reference offer made by other party)
  - `c`:	Comparisons to prices of external stuff (price of comparable house, price of imaginary existing offers)
  - `r`:	Repetition of previous offer, non-committal
  - `e`:	End of negotiation via offer acceptance entering mutual common ground (e.g., offer given followed by, “That works for me, let’s do it.”) - explicitly only happens once.
- Firm or Soft 
  - `s`: Soft number (e.g., 220ish)
    - Suffixes: “-ish”, prefixes: “around”, etc.
  - `f`: Firm number
- External Incentive
  - `y`:	speaker incorporates as a part of the offer non-monetary incentives (landscaping, sale/offer timing, cash payment of amount vs mortgage), needs to reference an offer.

### Anonymizing

We replaced all occurences of participant names with the token `[PERSON]`.

## Citation

If you use this dataset in your research or publication, please cite it as:

```
@inproceedings{heddaya-etal-2023-language,
    title = "Language of Bargaining",
    author = "Heddaya, Mourad  and
      Dworkin, Solomon  and
      Tan, Chenhao  and
      Voigt, Rob  and
      Zentefis, Alexander",
    booktitle = "Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2023",
    address = "Toronto, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.acl-long.735",
    pages = "13161--13185",
}
```
