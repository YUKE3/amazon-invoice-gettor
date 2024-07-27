from openai import OpenAI
from dotenv import load_dotenv


class gpt:

    def __init__(self):
        load_dotenv()
        self.client = OpenAI()

    def summarizeOrder(self, items):
        res = []

        for item in items:
            completion = self.client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[
                    {"role": "system", "content": "You are a logistics assistant, who is summarizing item names from invoices into short (less than 3 words) names describing what the item is."},
                    {"role": "user", "content": item}
                ]
            )

            res.append(completion.choices[0].message.content)

        return res
