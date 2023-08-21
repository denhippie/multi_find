# multi_find
Search for loads of substrings in a given string using a compiled index.

This is a toy project I did when I was bored on a flight to the US and had to stay awake.
The use case I was thinking of: let's say we have a surveillance monitor that needs to check messages
for many (thousands) of banned words or phrases. And we're surveilling for many many messages.
In that case te performance of looking for te banned words matter. Doing the brute force substring in string check of Python is likely a bottleneck.
You can of course also just create a regex with all those words in a single compiled regex and use that. However, that didn't turn out to be any imporvement.
I wrote a simple datastructure to contain all the search words and a simple way to search in given messages for the words in the list.
At the time of writing I get close to a 10x improvement.

