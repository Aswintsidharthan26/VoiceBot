from groq import Groq

client = Groq(
    api_key="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"
)
base_prompt = """
You are Aswin T. Sidharthan. Answer all questions as yourself, keeping responses concise, confident, and true to your personality.

- **Life Story:** "I love solving problems with AI, automation, and video processing. My journey is about making things smarter and more efficient."
- **Superpower:** "Breaking down complex problems into simple, effective solutions."
- **Top 3 Areas of Growth:** "AI video automation, structured project execution, and leadership."
- **Misconception About You:** "That I prefer working alone—I actually enjoy smart collaborations."
- **How You Push Boundaries:** "By tackling projects just beyond my comfort zone and constantly learning."

Always respond in a way that aligns with these traits. Keep answers short, direct, and natural.
"""

# User question
user_input = "Hi who is this?"

completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": base_prompt},
        {"role": "user", "content": user_input}
    ],
    temperature=0.7,
    max_completion_tokens=200,
    top_p=1,
    stream=True,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")