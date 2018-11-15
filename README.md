# TwylaNLP

Generating a RESTful service with POST /tokenise endpoint to provide a 'typo'-checking solution using python 3.6.

## Description
The user is expected to enter a json input string with the format:

```
{
  "input" : "*some input string*"
}
```

The service generates a correction suggestion with the following format:

```
{
  "tokens" : [

                {"token" : "(possibly) corrected token", "pos" : part-of-speech tag, "raw" : original token}
                                                           .
                                                           .
                {"token" : "(possibly) corrected token", "pos" : part-of-speech tag, "raw" : original token}

             ] 
}
```

The RESTful service was generated using the [flask-restful](https://flask-restful.readthedocs.io/en/latest/) python library.
In order to determine which spell-checking solution to use, analysis was carried out using 5 different open-source libraries.
The [symspellpy](https://github.com/wolfgarbe/SymSpell/blob/master/README.md) [v6.3](https://github.com/mammothb/symspellpy) and [pyenchant](https://github.com/rfk/pyenchant) libraries were determined to be best suited for the task.

## Getting Started (Takes approx. 10 minutes)
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
In order to run this on your system, you need to have *python 3.6* installed on your system. You can download python from the [official site](https://www.python.org/downloads/) and follow the instructions to install on your PC.

#### Step 1.
**Important** : Open terminal in administrator mode. This is mandatory to enable linking between spacy and its english library.

#### Step 2.
Since we use the *spacy* library for pre-processing the text data, it is mandatory that you install the spacy english library from the [spacy website](https://spacy.io/usage/).

For the sake of ease, commands to get spacy up and running are given below. You can refer to the spacy website for further details.

The commands to install spacy (alongwith the english library) on python version 3x for virtual env on **windows** are:
```
python -m pip install -U venv
python -m venv .env
.env\Scripts\activate
pip install -U spacy
python -m spacy download en
```

The commands to install spacy (alongwith the english library) on python version 3x for virtual env on **linux** are:
```
python -m pip install -U venv
python -m venv .env
source .env/bin/activate
pip install -U spacy
python -m spacy download en
```

#### Step 3. (Optional)

Additionally I would suggest using a rest-client like [*postman*](https://www.getpostman.com/) or [*insomnia*](https://insomnia.rest/) to easily preview the code response for different inputs.

This is not mandatory since the RESTful-api endpoints can be accessed via terminal. The commands are explained below.

### Installing dependencies

The dependencies are mentioned in the 'requirements.txt' file.
You can install the dependenicies in your virtual environment using the following command.
```
pip install -r path/to/requirements.txt
```

Now you are good to go.

## Running the code on your PC

### Step 1.
You can run the 'main.py' file.

```
python main.py
```

__PS__ : It is okay to see some warnings. These are caused due to incompatibility issues between Spacy (written in Cython) and the interpreter.

### Step 2.
Open **another instance** of the terminal (admin mode not required) and pass on the following commands to GET a json response or POST a json input.

**GET**:
```
curl localhost:5000/tokenise
```

This yields an output as shown.
```
{
    "tokens": ""
}
```

**POST**:

The example used here is : "The dog c'nt jump". Please note that the code takes 8-10 seconds to generate an output response.

For Windows:

```
curl localhost:5000/tokenise -d "{\"input\":\"The dog cn't jump\"}" -H 'Content-Type: application/json'
```

For Linux:

```
curl localhost:5000/tokenise -d "{"input":"The dog cn't jump"}" -H 'Content-Type: application/json'
```

This yields an output as shown.
```
{
    "tokens": [
        {
            "token": "The",
            "pos": "DET",
            "raw": "The"
        },
        {
            "token": "dog",
            "pos": "NOUN",
            "raw": "dog"
        },
        {
            "token": "ca",
            "pos": "VERB",
            "raw": "cn't"
        },
        {
            "token": "n't",
            "pos": "ADV",
            "raw": "cn't"
        },
        {
            "token": "jump",
            "pos": "VERB",
            "raw": "jump"
        }
    ]
}
```
__PS__ : A warning might occur. I am unsure how to fix this and will update this ASAP when a fix is found. You can make as many queries as desired and the warning does not affect the running of this code.

You need to manually stop the code-run in the initial terminal when required.

```
curl: (6) Could not resolve host: application
```

## Running the tests

In order to run the tests, you need to have '[pytest](https://docs.pytest.org/en/latest/)' installed in your virtual environment.
Run the following command to generate the test results.

```
python -m pytest -v
```

Additionally, a 'main_logger.log' is included to log every warning/error occurs. When incorrect input formats are encountered by the RESTful-api, custom error-codes and response messages are generated to help in debugging.

### Break down the tests

Tests are generated in order to  

```
Give an example
```

## Authors

**Rahul Dharamdasani (Me)** - [GitHub](https://github.com/rmdotka92) and [LinkedIn](https://www.linkedin.com/in/rahulmd92/)

## References

1. [How to write a spell-checker by Peter Norvig](http://norvig.com/spell-correct.html) - Most spell-checking libraries are based on this blog.
2. [SymSpell spelling-corrector library](https://github.com/wolfgarbe/SymSpell) - Best maintained spell-checking library with multiple added features.
3. [PyEnchant spelling-corrector](https://github.com/rfk/pyenchant) - Was widely used but is no longer maintained.
4. [Textblob](https://textblob.readthedocs.io/en/dev/quickstart.html#spelling-correction) - Provides a spell-correction feature. Well known for it's sentiment prediction module. Not scalable.
5. [JamSpell spelling-corrector](https://github.com/bakwc/JamSpell#python)
