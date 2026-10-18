"""Real OpenAI SDK example. No API call without explicit --live.

python live_api_chatbot.py --live --api chat
python live_api_chatbot.py --live --api responses
Key and model are read from environment. Never print the key.
"""
import argparse
import os
import sys

INSTRUCTIONS = 'Объясняй ML начинающему на русском. Давай краткий пример и ограничение.'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--api', choices=['chat', 'responses'], default='chat')
    args = parser.parse_args()
    if not args.live:
        print('No API call. Follow LIVE_API_LAB.md, then pass --live explicitly.')
        return 0
    if not os.environ.get('OPENAI_API_KEY') or not os.environ.get('OPENAI_MODEL'):
        print('Set OPENAI_API_KEY and OPENAI_MODEL in your local environment.', file=sys.stderr)
        return 2
    try:
        import openai
        from openai import OpenAI
    except ImportError:
        print('Install the optional openai SDK from requirements-live.txt.', file=sys.stderr)
        return 2
    # SDK handles bounded retry for transient errors. No nested retry loop here.
    client = OpenAI(timeout=30.0, max_retries=2)
    model = os.environ['OPENAI_MODEL']
    turns = []
    print('Live API mode. Requests may incur usage charges. /quit exits, /reset clears local history.')
    try:
        while True:
            try:
                text = input('You> ').strip()
            except EOFError:
                break
            if text == '/quit':
                break
            if text == '/reset':
                turns.clear()
                print('Local history cleared.')
                continue
            if not text:
                continue
            # Last four complete turns; not an exact tokenizer budget.
            candidate = turns[-8:] + [{'role': 'user', 'content': text}]
            try:
                if args.api == 'chat':
                    response = client.chat.completions.create(
                        model=model,
                        messages=[{'role': 'system', 'content': INSTRUCTIONS}] + candidate,
                        store=False,
                    )
                    if not response.choices:
                        raise ValueError('Empty choices')
                    choice = response.choices[0]
                    answer = choice.message.content
                    if choice.finish_reason != 'stop':
                        raise ValueError('Incomplete response: ' + str(choice.finish_reason))
                else:
                    response = client.responses.create(
                        model=model, instructions=INSTRUCTIONS, input=candidate, store=False,
                    )
                    if response.status != 'completed':
                        raise ValueError('Incomplete response: ' + str(response.status))
                    answer = response.output_text
                if not isinstance(answer, str) or not answer.strip():
                    raise ValueError('Empty text / refusal / non-text result; inspect contract.')
            except openai.AuthenticationError:
                print('Authentication failed. Correct credentials; request not added to history.')
                continue
            except openai.BadRequestError:
                print('Bad request. Check model capabilities and message schema.')
                continue
            except openai.RateLimitError:
                print('Rate/quota limit after bounded SDK retries. Check quota before retrying.')
                continue
            except openai.APIConnectionError:
                print('Connection/timeout failure. Check connectivity; history unchanged.')
                continue
            except openai.APIStatusError as error:
                print('API status:', error.status_code, 'request_id:', getattr(error, 'request_id', None))
                continue
            except ValueError as error:
                print('Response validation:', error)
                continue
            turns = candidate + [{'role': 'assistant', 'content': answer}]
            print('Assistant>', answer)
            if response.usage is not None:
                print('Actual usage:', response.usage.model_dump())
    finally:
        client.close()
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
