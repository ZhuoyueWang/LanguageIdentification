# LanguageIdentification
##  LING 406 MP2
### Zhuoyue Wang, zhuoyue2

Files:

LangId.train.English, LangId.train.French, LangId.train.Italian: Input files with same content in different languages
LangId.test, LangId.sol: testing data set and its labels
letterLangId.py: The program about question 1, which creates a letter bigram model with add-one smoothing to test testing data set
wordLangId.py: The program about question 2, which creates a word bigram model with add-one smoothing to test testing data set
wordLangId2.py: The program about question 2, which creates a word bigram model with Jelinek-Mercer smoothing to test testing data set
letterLangId.out, wordLangId.out, wordLangId2.out: The output files made by three models above


How to run:

Be sure in the working directory which contains these files and type "python3 letterLangId.py", "python3 wordLangId.py",
"python3 wordLangId2.py" in the terminal. The output will be appeared in letterLangId.out, wordLangId.out, wordLangId2.out. The terminal will print out their accuracy


Question 1:

Yes. The letter bigram can be implemented without smoothing, which the accuracy is 87% ran by my program. But within add-one smoothing, the accuracy increases to 98%. The reason to do smoothing is that the bigram model may meet trouble when it meets the unseen words. It leads to the change

Question 2:

Compared with the solution file, my word bigram model has 99% accuracy, which is really high. I tested it 5 times and got the same result.

Analysis:

Under the same smoothing method, the word bigram model has higher accuracy (99%) is slightly higher than that of the letter bigram (98%). The advantage of word bigram model (Model in Question 2) is words in different languages are significantly different from each other. Therefore, when we have a word bigram model trained by sufficiently large data set, it is easy to distinguish from each other language according to vocabulary difference. Also, after tokenization of sentences, the word bigram model will have shorter sequences and make the task easier because it can account the dependencies between fewer tokens over less time-steps. Another issue on letter bigram model I want to mention is that the letter model need to learn spelling in addition to syntax, semantics, etc. In any case, word language models will typically have lower error than letter models.

However, there is still a main advantage of character over word language models, which is that they have a really small vocabulary. It leads to character models will require less memory and have faster inference than their word counterparts. Another advantage is that they do not require tokenization as a preprocessing step.


Question 3 (Extra Credit):

I create a word bigram model with Jelinek-Mercer smoothing. Jelinek-Mercer smoothing has a parameter lamda to adjust the performance of the smoothing function. When I set lamda = 0.985, the accuracy result is 0.993333, which is higher than the result of question 2.

For the analysis part, I would like to mention more about the difference between using add-one smoothing and Jelinek-Mercer smoothing. One of the disadvantages on add-one smoothing is that it moves too much probability mass from seen to unseen events and assigns too much total probability mass to unseen events, which is too simplistic. One of the advantage of Jelinek-Mercer smoothing is using linear interpolation between n-order ML model and n-1-order smoothed model. It also has a parameter lamda to adjust the model performance depend on the context of text data, which is really flexible. 
