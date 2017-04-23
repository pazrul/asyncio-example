if env | grep -q ^CONFIG_FILE=
then
  echo env variable is already exported
else
  echo env variable was not exported, but now it is
  export CONFIG_FILE=config/dev.toml
fi

python main.py
export CONFIG_FILE=''
