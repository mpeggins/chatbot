This project demonstrates how to build a simple chatbot using a Gemini API.

## Updates:

This is version 2 of the project.

In this version, we implement a simple iterative chat feature. As opposed to sending a manual prompt each time, we are now able to have a back and forth conversation with the model. 

###  Configurations:

In this version, we implemented new chat configurations. **These are not strictly necessary, but it does allow you more control over the system's responses.** Here are the configurations explained:

#### Temperature:
    temperature=0.5

The valid range for Temperature is from 0.0 to 2.0. 

Temperature controls the degree of randomness in token selection. Higher temperatures result in a higher number of potential tokens and can produce more creative results, while lower temperatures have the opposite effect, such that a temperature of 0 results in greedy decoding, selecting the most probable token at each step.

Temperature doesn't provide any guarantees of randomness, but it can be used to "nudge" the output.

#### Maximum number of tokens:
    max_output_tokens=300

This can be any number you decide. Importantly, this is a hard stop. It does not mean the model will generate a response less than the specified characters. It means that it will stop generating its response once it reaches this number.

#### Top P:
    top_p=0.95

Top P works by selecting from the most probable tokens whose cumulative probability adds up to the `top_p` value. For example, a `top_p` of `0.95` means the model will only consider tokens from the most likely 95% of the probability distribution.

#### Top K:
    top_k=40

Top K works by selecting from the `top_k` most likely tokens. For example, a `top_k` of `40` means the model will only consider the 40 most probable next tokens, regardless of their cumulative probability.

When using both `Top P` and `Top K`, the model will apply whichever filter results in a smaller, more restrictive set of tokens.

**NOTE:** In practice, developers typically decide to use *either* Top P *or* Top K, not both. This project serves to demonstrate possibilities.

## Limitations:

This version strictly uses Gemini's knowledge base. It does not work with any proprietary data, i.e. there are no RAG features.

In the following version of this project, we will implement actual RAG features to chat with your own data.