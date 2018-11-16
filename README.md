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
  "tokens" : [{"token" : "(possibly) corrected token", "pos" : part-of-speech tag, "raw" : original token}
                                                         .
              {"token" : "(possibly) corrected token", "pos" : part-of-speech tag, "raw" : original token}]
}
```

The RESTful service was generated using the [flask-restful](https://flask-restful.readthedocs.io/en/latest/) python library.
In order to determine which spell-checking solution to use, analysis was carried out using 5 different open-source libraries.
The [symspellpy](https://github.com/wolfgarbe/SymSpell/blob/master/README.md) [v6.3](https://github.com/mammothb/symspellpy) and [pyenchant](https://github.com/rfk/pyenchant) libraries were determined to be best suited for the task.

__PS__: I have included all necessary instructions, commands and links in this readme file. 

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

This is not mandatory since the RESTful-api endpoints can be accessed via terminal. The commands are included below.

### Installing dependencies

The dependencies are mentioned in the 'requirements.txt' file.
You can install the dependencies in your virtual environment using the following command.
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

__PS__ : It is okay to see some warnings. These are caused due to incompatibility issues between Spacy (written in Cython) and the interpreter. Once the warnings stop popping on your terminal, you can move on to the next step.

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
curl localhost:5000/tokenise -d "{\"input\":\"The dog cn't jump\"}" -H 'Content-Type:application/json'
```

For Linux:

```
curl localhost:5000/tokenise -d "{"input":"The dog cn't jump"}" -H 'Content-Type:application/json'
```

This yields an output as shown.
```
{
    "tokens": [{"token": "The", "pos": "DET", "raw": "The"},
               {"token": "dog", "pos": "NOUN", "raw": "dog"},
               {"token": "ca", "pos": "VERB", "raw": "cn't"},
               {"token": "n't", "pos": "ADV", "raw": "cn't"},
               {"token": "jump", "pos": "VERB", "raw": "jump"}]
}
```
You need to manually stop the code-run in the initial terminal when required.

__PS__ : The character max-limit is set to 100 per POST request.

## Running the tests

In order to run the tests, you need to have '[pytest](https://docs.pytest.org/en/latest/)' installed in your virtual environment.
Run the following command to generate the test results.

```
python -m pytest -v
```

Additionally, code coverage report can be generated using the following line of code (requires 'pytest-cov' to be installed).
```
python -m pytest --cov -v
```

Here's a how the test-result looks like:

Inline-style: 
![alt text](https://github.com/rmdotka92/TwylaNLP/blob/master/tests/test_coverage_report.jpg "Test and coverage report")

A 'main_logger.log' is included to log every warning/error that occurs. When incorrect input formats are encountered by the RESTful-api, custom error-codes and response messages are generated to help in debugging.

### Summary of the tests

Tests are designed to account for proper functioning and proper error responses of different modules. Additionally, 2 integration tests are run to check how different modules interact with each other. There are 3 important modules, namely,

1. pre-processing
2. dictionary (sym-spellpy or enchant)
3. post-processing

Each of these modules are tested individually and in conjunction with each other.

## Description of the spelling library used, success and failure cases (optional)

The spelling library used here is SymSpell. The reason for choosing this is because it seemed to give decent results, is widely popular, is constantly being updated by it's creator and the python NLP community and has shown impressive results in comparison to other spell-checking/correction libraries.

Almost all spell-checking libraries are based on Peter Norvig's blog (see References). The blog explains how to generate possible spell-checks based on *edit-distance*. SymSpell is **word-frequency based** and not a **context-based** spell-checking library. Note that in my implementation, the response is generated after 8-10 seconds. This is because I looped over each token in order to disable spell-checking on Proper Nouns and on words smaller than 2 characters. Without these forced conditions, the library would try to correct names and change the alphabet 'I' to 'a'. This would change a sentence like **'Rahul and I are good frinds'** to **'Paul and a are good friends'**. Each time a token is tested, a reference dictionary is built from the existing corpus list and this leads to added run-time. 

Pyenchant is another decent library. It does the job fast and does manage to produce good results. Unfortunately, it is no longer maintained. It has also been observed that it does not install well on 64-bit OS. I have included the code in my 'main.py' file. In case, pyenchant can be installed on your PC after running the following command,

```
pip install pyenchant
```
you can add the following line to the main.py file and set the variable **DEFAULT = 0** in both, 'main.py' and 'test_main.py'.

```
import enchant
```
The code should run fine.

### SUCCESS CASES
- Successfully corrects (upto a certain degree of accuracy) sentences with proper nouns, apostrophes and single-letter words like I,a.
- Successfully mirrors the case of the first alphabet of the word in the output (**Appl** --> **Apple** but **APPL** --> **apple**). 

This is because the spell-checking algorithms are case-sensitive. Hence it is necessary that the token-cases are set to lowercase before processing and set back to the original state at the output.

### FAILURE CASES
- Fails to detect punctuation. (Seems tricky. Need more time.)
- Fails to mirror the exact case.
- Fails to make context-based corrections.


## Authors

**Rahul Dharamdasani (Me)** - [GitHub](https://github.com/rmdotka92) and [LinkedIn](https://www.linkedin.com/in/rahulmd92/)

## References

1. [How to write a spell-checker by Peter Norvig](http://norvig.com/spell-correct.html) - Most spell-checking libraries are based on this blog.
2. [SymSpell spelling-corrector library](https://github.com/wolfgarbe/SymSpell) - Best maintained spell-checking library with multiple added features.
3. [PyEnchant spelling-corrector](https://github.com/rfk/pyenchant) - Was widely used but is no longer maintained.
4. [Textblob](https://textblob.readthedocs.io/en/dev/quickstart.html#spelling-correction) - Provides a spell-correction feature. Well known for it's sentiment prediction module. Not scalable.
5. [Pyspellchecker](https://github.com/barrust/pyspellchecker)
6. [JamSpell spelling-corrector](https://github.com/bakwc/JamSpell#python)

