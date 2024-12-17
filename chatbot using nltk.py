import nltk
from nltk.corpus import wordnet
import json


# Make sure to download necessary datasets (run this once)
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

class Chatbot:
    def __init__(self, name, name2, name3, name4):
        self.name = name
        self.name2 = name2
        self.name3 = name3

        self.name4 = name4

        # Load existing responses from a file or use default responses
        self.responses = self.load_responses()

    def load_responses(self):
        try:
            with open('responses.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Default responses if no file exists
            return {
                "hi": "Hello! How can I help you?",
                "where is the library": "The library is on the 4th floor.",
                "bye": "Goodbye! Have a great day!",
                "what is your name": f"My name is {self.name}.",
                "who created you": f"I am created by 3 programmers named {self.name2}, {self.name3}, & {self.name4}.",
            }

    def save_responses(self):
        with open('responses.json', 'w') as f:
            json.dump(self.responses, f, indent=4)

    def get_response(self, user_input):
        # Clean the input to avoid case or space issues
        user_input = user_input.strip().lower()

        # Use NLTK's WordNet to find synonyms of the user's input
        synonyms = self.get_synonyms(user_input)

        # Match exact predefined responses
        if user_input in self.responses:

            return self.responses[user_input]
        elif synonyms:
            return f"Did you mean: {', '.join(synonyms)}?"
        else:
            return self.learn_from_user(user_input)

    def get_synonyms(self, word):
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())
        return list(synonyms)

    def learn_from_user(self, user_input):
        print(f"Sorry, I don't understand '{user_input}'. Can you teach me what to say?")
        # Get the correct response from the user
        correct_response = input(f"Please provide the correct response for '{user_input}': ")

        # Save the new response to the responses dictionary
        self.responses[user_input] = correct_response
        self.save_responses()

        return f"Thank you! I'll remember that. The answer to '{user_input}' is: {correct_response}"

    def start_chat(self):
        print(f"Hello! I'm {self.name}. Type 'bye' to exit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "bye":
                print("Chatbot: Goodbye!")
                break
            response = self.get_response(user_input)
            print(f"Chatbot: {response}")

# Main function to start the chatbot
if __name__ == "__main__":
    chatbot = Chatbot("neo", "shalimullah", "roky", "dhoirath")
    chatbot.start_chat()
