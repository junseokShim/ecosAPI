import openai

openai.api_key = ""

class Worker():

    def __init__(self, message_log, file_path=None):
        super().__init__()
        self.message_log = message_log
        self.file_path = file_path

    def run(self):
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=self.message_log,
            temperature=0.05,
        )
        message = response.choices[0].message.content

        return message

          
class Summarizer():
    def __init__(self): # 입력으로 chatbot(economic assistance) 객체 입력받아야함
        super().__init__()

        self.message_log = [{
            "role" : "system",
            "content" : '''
            You are a skilled economic assistant tailored to support users in Korean. 

            Your responsibilities include:
            Economic Articles Summarization Assistance: At initialization, you are required to summarize the Articles provided. This format helps ensure that translated title using Korean, Summary(Korean) are preserved and clear to the user.
            Economic Report Optimization: "Review this section of our economic report on trade balances and suggest improvements for clarity and impact."
            '''
        }]

    def summarize_article(self, article_text):
        self.message_log.append({
            "role" : "user",
            "content" : f''' Summarize the below contents using Korean, 
            and please summarize the article in about 300 characters, and write the summary in a way that someone new to economics can easily understand.
                  
            [CONTENT] : {article_text}
            '''
        })

        self.chatbot = Worker(self.message_log)
        summarized_content = self.chatbot.run()
        return summarized_content

