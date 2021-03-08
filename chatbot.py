from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Creating ChatBot Instance
chatbot = ChatBot('Moodle Bot',
                   storage_adapter='chatterbot.storage.SQLStorageAdapter',
                   database_uri='sqlite:///database.sqlite3')

 # Training with Personal Ques & Ans 
training_data_quesans = open('training_data/ques_ans.txt').read().splitlines()
training_data_personal = open('training_data/personal_ques.txt').read().splitlines()

training_data = training_data_quesans + training_data_personal

trainer = ListTrainer(chatbot)
trainer.train(training_data) 


# Training with English Corpus Data 
trainer_corpus = ChatterBotCorpusTrainer(chatbot)
trainer_corpus.train(
    'chatterbot.corpus.english'
) 