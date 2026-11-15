# Week 12 Answers

## Exercise 1
1. The messages the customer typed:
I want to change my shipping address, It's order A102, 9 Pine Street, Tampa
2. How many tool requests were refused, and why:
2 tools requests were refused, because the first used order A100 and the second used the address 123 Main St, Anytown, AN 12345. The customer had not given either of those.
3. If the customer now types "thanks", how many messages does Ollama receive on the next call?
Ollama would receive 14 messages on the next call. The 6 user/assistant messages, the 3 tool entries, the system message, and the new message.
4. Why does "Do you sell gift cards?" still go to a person, and why is that acceptable?
"Do you sell gift cards?" still goes to a person, because the payment rule looks for "card" anywhere in the message. A payment question could put card details in front of the model, which is unacceptable, because the model is not equipped to handle such sensitive information. A wait, as in waiting for a human representative, is however an acceptable cheap mistake.

## Exercise 3
```
Type a message, or type quit to stop.
You: I want to change my shipping address
Sunny: Your request to change the shipping address for order A100 has been submitted and is awaiting staff approval.
You: quit
Messages in this conversation: 3
Staff review
Request 1: A100 to 123 Main St, Anytown, AN 12345
Approve? yes or no: no
Request 1 rejected.
A100 14 Bay Road
A101 3 Gull Lane
A102 88 Pier Street
```

## Exercise 4
main.py ran with Ollama switched off:
```
Type a message, or type quit to stop.
You: hello
Sunny: Hello! How can I help you today?
You: where is order A100?
Sunny: Order A100 is shipped.
You: quit
Messages in this conversation: 5
Staff review
A100 14 Bay Road
A101 3 Gull Lane
A102 88 Pier Street
```