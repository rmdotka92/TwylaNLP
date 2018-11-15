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

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
In order to run this on your system, you need to have *python 3.6* installed on your system. You can download python from the [official site](https://www.python.org/downloads/) and follow the instructions to install on your PC.

Since we use the *spacy* library for pre-processing the text data, it is mandatory that you install the spacy english library from the [spacy website](https://spacy.io/usage/).

For the sake of ease, commands to get spacy up and running are given below. You can refer to the spacy website for further details.

The commands to install spacy (alongwith the english library) on python version 3x for virtual env on windows are:
```
python -m pip install -U venv
python -m venv .env
.env\Scripts\activate
pip install -U spacy
python -m spacy download en
```

The commands to install spacy (alongwith the english library) on python version 3x for virtual env on linux are:
```
python -m pip install -U venv
python -m venv .env
source .env/bin/activate
pip install -U spacy
python -m spacy download en
```

Recommended:
Additionally I would suggest using a rest-client like [*postman*](https://www.getpostman.com/) or [*insomnia*](https://insomnia.rest/) to easily preview the code response for different inputs.

### Installing

The dependencies are mentioned in the 'requirements.txt' file.
You can install the dependenicies using the following command from your virtual environment.
```
pip install -r path/to/requirements.txt
```
Now you are good to go.
You can run the main.py file.

```
python main.py
```
Open another instance of the command prompt and pass on the following commands to GET a json response or POST an input.

POST:
```
curl localhost:5000/tokenise -d "{\"input\":\"The dog cn't jump over Jacob\"}" -H 'Content-Type: application/json'
```


## Running the tests

```

```

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```
## Built With


## Authors

* **Rahul Dharamdasani (Me)** -  [github](https://github.com/rmdotka92)
                              -  [linkedin](https://www.linkedin.com/in/rahulmd92/)

## References

