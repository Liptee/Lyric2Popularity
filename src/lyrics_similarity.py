import re
import math
from collections import Counter
from typing import Tuple

_WORD_RE = re.compile(r"[a-zа-яё0-9]+")

def _normalize(text: str) -> Tuple[str, ...]:
    """Нижний регистр → рус./англ. буквы+цифры, убираем дубликаты строк."""
    # 1) построчно, чтобы убрать подряд идущие повторы (припевы)
    seen, cleaned = set(), []
    for line in text.lower().splitlines():
        line = " ".join(_WORD_RE.findall(line))  # оставить слова/цифры
        if line and line not in seen:
            cleaned.append(line)
            seen.add(line)
    return tuple(cleaned)

def _vectorize(lines: Tuple[str, ...]) -> Counter:
    """unigram + bigram частоты"""
    bag = Counter()
    for line in lines:
        words = line.split()
        bag.update(words)                       # униграммы
        bag.update(zip(words, words[1:]))       # биграммы как кортежи
    return bag

def lyrics_similarity(text1: str, text2: str) -> float:
    """
    0.0 → совсем разные, 1.0 → идентичны (после нормализации).
    """
    v1, v2 = _vectorize(_normalize(text1)), _vectorize(_normalize(text2))
    if not v1 or not v2:                # один из текстов пуст после чистки
        return 0.0

    # косинусное сходство
    common = set(v1) & set(v2)
    dot   = sum(v1[t] * v2[t] for t in common)
    norm1 = math.sqrt(sum(n * n for n in v1.values()))
    norm2 = math.sqrt(sum(n * n for n in v2.values()))
    return dot / (norm1 * norm2)


if __name__ == "__main__":
    text1 = """
[Verse 1]
All the streets are crammed with things eager to be held
I know what hands are for, and I'd like to help myself
You ask me the time, but I sense something more
And I would like to give you what I think you're asking for

[Pre-Chorus]
You handsome devil
Oh, you handsome devil

[Chorus]
Let me get my hands
On your mammary glands
And let me get your head
On the conjugal bed
I say, I say, I say

[Verse 2]
I crack the whip and you skip
But you deserve it, you deserve it, deserve it, deserve it
A boy in the bush is worth two in the hand
I think I can help you get through your exams

[Pre-Chorus]
Oh, you handsome devil

[Chorus]
Oh, let me get my hands
On your mammary glands
And let me get your head
On the conjugal bed
I say, I say, I say

[Verse 3]
I crack the whip, you skip
But you deserve it, you deserve it, deserve it, deserve it
And when we're in your scholarly room, who will swallow whom?
And when we're in your scholarly room, who will swallow whom?

[Pre-Chorus]
You handsome devil

[Chorus]
Oh, let me get my hands
On your mammary glands
And let me get your head
On the conjugal bed
I say, I say, I say

[Outro]
There's more to life than books, you know
But not much more
There's more to life than books, you know
But not much more, not much more
Oh, you handsome devil
Oh, you handsome devil
Oh!"""

    text2 = """[Verse 1]
All the streets are crammed with things eager to be housed
And I know what hands are for
And I'd like to help myself
And you ask me the time
And I sense something more
And I would like to give you what I think you're asking for
You handsome devil
Oh, you handsome devil

[Chorus]
Let me get my hands
On your mammary glands
And let me get your head in a conjugal bed
I said, I said, I said

[Verse 2]
I crack the whip and you skip but you deserve it
You deserve it, deserve it, deserve it
A boy in the bush is worth two in the hand
I think I can help you get through your exams
Oh, you handsome devil

[Chorus]
Let me get my hands
On your mammary glands
And let me get your head in a conjugal bed
I said, I said, I said

[Verse 3]
I crack the whip and you skip but you deserve it
You deserve it, deserve it, deserve it
And when we're in your scholarly room
Who will swallow whom?
And when we're in your scholarly room
Who will swallow whom?
You handsome devil

[Bridge]
And I know a place
Where no one is likely to pass
And you don't care if it's late
And you don't care if you're lost
And though you don't agree
Well, you don't refuse
If it's the last thing that I ever do
I'm gonna get you

[Chorus]
You handsome devil
Let me get my hands
On your mammary glands
And let me get your head in a conjugal bed
I said, I said, I said

[Verse 4]
There's more to life than books you know
But not much more
Oh, there's more to life than books you know
But not much more, not much more
Oh, you handsome devil
Oh, oh, you handsome devil"""
    print(lyrics_similarity(text1, text2))