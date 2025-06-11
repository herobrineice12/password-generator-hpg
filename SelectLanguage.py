from .script.Action import ask
from Main import main

language = ask("English/Português? (0,1): ")
if language:
    main(language)