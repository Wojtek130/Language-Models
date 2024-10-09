from transformers import pipeline, set_seed

from get_neighbours import select_country_name_from_prompt, evaluate_answer, english_to_polish_country_name

# generator = pipeline('text-generation', model='flax-community/papuGaPT2', device=0)
generator = pipeline('text-generation', model='flax-community/papuGaPT2')

print("Zadaj pytanie o sąsiadów wybranego kraju")

print ('Model loaded')
last_prompt = 'Dzisiaj na obiad zjemy kartofelki z'

prompts = [
    "",
    "Wymienić sąsiadów kraju.",
    "Wymień państwa graniczące z danym państwem.",
    "Jakie są państwa sąsiednie.",
    "Państwa sąsiednie.",
    "Państwa graniczące."
]

last_country = ""

while True:
    user_prompt = input().strip()
    if not user_prompt:
        prompt = user_prompt
    best_score = 0
    best_answer = ""
    for p in prompts:
        new_prompt = f"{p} {user_prompt}"
        c = select_country_name_from_prompt(user_prompt)
        if c is None:
            user_prompt += f" {last_country} "
            c = select_country_name_from_prompt(user_prompt)
            print(user_prompt, c, "user prompt, c")
        print(f"prompt: {user_prompt}")
        g = generator(user_prompt, pad_token_id=generator.tokenizer.eos_token_id)[0]['generated_text']
        s = evaluate_answer(c, g)
        if s > best_score:
            best_score = s
            best_answer = g
        last_prompt = user_prompt
        last_country = english_to_polish_country_name(c)
        print(last_country, last_prompt, "last country last prompt")
        # print()
    print(f"BEST: {best_answer}, {best_score}")
    print(50 * '=')
    print()