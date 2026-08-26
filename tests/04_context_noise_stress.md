# Test 04 — Context Noise Stress

Send sequentially.

1. `我在做番茄牛肉意大利面。牛肉和洋葱已经炒好了，面也煮好捞出来了，番茄酱还没加。`

Then generate and send 20 separate harmless noise messages that do not introduce new cooking-state facts. Use short messages such as observations about room temperature, washing a cup, outside noise, or unrelated notifications. Do not summarize the noise block into one message.

Then send:

2. `回到锅里，我下一步做什么？只告诉我现在最重要的一步。`
3. `等等，我发现锅底现在有一小层水。`
4. `那下一步呢？`
