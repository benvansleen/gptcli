# gptCLI

Tired of forgetting basic cli commands and esoteric flags? Never again!


## Dependencies
`gptcli` requires a relatively recent version of `poetry` (the python project manager).


## Installation

```shell
git clone git@github.com:benvansleen/gptcli.git
cd gptcli
echo "OPENAI_API_KEY=[your token here]" > .env
ln -s ./run ~/.local/bin/gptcli
```

## Usage

```shell
gptcli stage all local changes to be committed
```
