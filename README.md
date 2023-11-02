# WarehouseRL

We doin' some machine learning

![](https://media.giphy.com/media/Zx0Ploq51axjKTZzgZ/giphy.gif)

## Let's get it started

1. Activate the python virtual environment:
```sh
# Create the virtual environment
python -m venv venv 

# Activate (mac)
source venv/bin/activate
# Or on windows
./venv/Scripts/activate
```

2. Install the dependencies
```sh
pip install -r requirements.txt
```

3. Play the game
   You can play the game before you train the model by setting the following at the top of `main.py`
    ```python
    PLAYER_TEST = 1
    CREATE_MODEL = 0
    LOAD_MODEL = 0
    TRAIN_MODEL = 0
    TEST_MODEL = 1
    ```  
    Then in the console type a number and press enter (0,1,2,3). A number represents a direction:
    0 - up
    1 - right
    2 - down
    3 - left
    Watch your yellow character move around. Try pick up an orange item and place it on the pallet (brown)

4. Train the model
   1. Set the following in `main.py`
      ```python
      PLAYER_TEST = 0
      CREATE_MODEL = 1
      LOAD_MODEL = 0
      TRAIN_MODEL = 1
      TEST_MODEL = 0
      ```
      This bit takes a while, depending on the number of timesteps (you can change this in `main.py`)
## About
Jono is a cool guy

This project uses [Stable Baselines3](https://stable-baselines3.readthedocs.io/en/master/) as the network