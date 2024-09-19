from openai import OpenAI
import time
from config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

class BaseAssistant:
    def __init__(self, assistant_id):
        self.assistant_id = assistant_id
        self.model = OPENAI_MODEL

    def create_thread(self):
        return client.beta.threads.create()

    def submit_message(self, thread, user_message):
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )
        return client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant_id,
        )

    def get_response(self, thread):
        messages = client.beta.threads.messages.list(thread_id=thread.id, order="asc")
        return [msg.content[0].text.value for msg in messages.data]

    def wait_on_run(self, thread, run):
        while run.status == "queued" or run.status == "in_progress":
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)
        return run

    def process_message(self, thread, user_message):
        run = self.submit_message(thread, user_message)
        run = self.wait_on_run(thread, run)
        return self.get_response(thread)[-1]  # Return the last message