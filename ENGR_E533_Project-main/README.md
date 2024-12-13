

## Self-Checkout Produce Identifier - Tentatively [MyProducePal](https://engr-e533-project.streamlit.app)

This project aims to streamline the self-checkout experience in grocery stores by leveraging computer vision to accurately identify fresh produce in real-time. Currently, customers must manually search for and select produce items like apples or bananas at self-checkout stations, which can slow down the process leading to frustration. This project replaces this manual process with a deep learning-based app which automatically identifies items using the checkout station’s built-in cameras.

### Problem
Self-checkout stations at stores like Kroger, Walmart, and Target require customers to manually enter or select fresh produce items, leading to:
- Slower checkout times
- Potential billing inaccuracies
- Frustration for customers

### Solution
This project builds a deep learning model to automatically identify produce based on images captured in real-time by the checkout station cameras. The app can recognize 141 different classes of fruits, vegetables, and nuts with high accuracy, significantly improving the checkout experience. In addition to checkout automation, this system can be used for:

- Sorting damaged produce
- Identifying ripe produce for sale at reduced prices
- Assisting with food waste reduction initiatives

### Dataset
The model is trained on the Fruits 360 dataset, which contains:

- 94,110 labeled images of fruits, vegetables, and nuts
- 141 classes
- Images are 100x100 pixels and include various angles and rotations
- Dataset: [Kaggle - Fruits 360](https://www.kaggle.com/datasets/moltean/fruits)

### Applications
- Improved self-checkout: Faster, more accurate produce identification
- Food sorting: Automatic detection of damaged or irregular produce
- Health integration: Identifying nutritional information for fresh produce


## Setup Instructions
<details open>
    
### Assumptions:
- git and python are installed already
- development locally is within VSCode 


### Steps:
- After cloning repo, when first opening VSCode, select global python interpreter to run venv setup scripts.

- Run install.py - this will setup the virtual environment and install all required packages. This may take a few minutes but only needs to be run one time. 
    If new dependencies are added during development to pyproject.toml then the install will need to be run again.

- Switch the python interpreter to the virtual environment.

- Optional: Install the recommended VSCode extensions. 

- Install Git LFS before working with large files
    ```bash
    # macOS
    brew install git-lfs

    # windows
    choco install git-lfs

    # Init after install
    git lfs install
    ```
</details>

## Running Streamlit
<details open>

- Streamlit runs from a few commands in a python script. Right now this is setup in test_streamlit.py

- Streamlit executes locally with the following command 

    ```bash
    streamlit run test_streamlit.py
    ```
    
- Access the hosted site with the following url
[MyProducePal](https://engr-e533-project.streamlit.app)

</details>


