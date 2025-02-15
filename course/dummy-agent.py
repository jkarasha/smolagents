import marimo

__generated_with = "0.11.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        """
        Serverless API

        In the Hugging Face ecosystem, there is a convenient feature called Serverless API that allows you to easily run inference on many models. There's no installation or deployment required.

        To run this notebook, you need a Hugging Face token that you can get from https://hf.co/settings/tokens. If you are running this notebook on Google Colab, you can set it up in the "settings" tab under "secrets". Make sure to call it "HF_TOKEN".

        You also need to request access to the Meta Llama models, if you haven't done it before. Approval usually takes up to an hour.
        """
    )
    return


@app.cell
def _():
    import os
    from dotenv import load_dotenv
    from huggingface_hub import InferenceClient

    load_dotenv()
    return InferenceClient, load_dotenv, os


@app.cell
def _(InferenceClient):
    client = InferenceClient("meta-llama/Llama-3.2-3B-Instruct")
    # if the outputs for next cells are wrong, the free model may be overloaded. You can also use this public endpoint that contains Llama-3.2-3B-Instruct
    #client = InferenceClient("https://jc26mwg228mkj8dw.us-east-1.aws.endpoints.huggingface.cloud")

    return (client,)


@app.cell
def _(client):
    # As seen in the LLM section, if we just do decoding, **the model will only stop when it predicts an EOS token**, 
    # and this does not happen here because this is a conversational (chat) model and we didn't apply the chat template it expects.
    client.text_generation(
        "The capital of france is",
        max_new_tokens=100,
    )
    return


@app.cell
def _(client):
    # If we now add the special tokens related to Llama3.2 model, the behaviour changes and is now the expected one.
    prompt="""<|begin_of_text|><|start_header_id|>user<|end_header_id|>

    The capital of france is<|eot_id|><|start_header_id|>assistant<|end_header_id|>

    """
    client.text_generation(
        prompt,
        max_new_tokens=100,
    )
    return (prompt,)


@app.cell
def _(client):
    client.chat.completions.create(
        messages=[
            {"role": "user", "content": "The capital of france is"},
        ],
        stream=False,
        max_tokens=1024,
    ).choices[0].message.content
    return


@app.cell
def _():
    # This system prompt is a bit more complex and actually contains the function description already appended.
    # Here we suppose that the textual description of the tools has already been appended
    SYSTEM_PROMPT = """Answer the following questions as best you can. You have access to the following tools:

    get_weather: Get the current weather in a given location

    The way you use the tools is by specifying a json blob.
    Specifically, this json should have a `action` key (with the name of the tool to use) and a `action_input` key (with the input to the tool going here).

    The only values that should be in the "action" field are:
    get_weather: Get the current weather in a given location, args: {"location": {"type": "string"}}
    example use :
    ```
    {{
      "action": "get_weather",
      "action_input": {"location": "New York"}
    }}

    ALWAYS use the following format:

    Question: the input question you must answer
    Thought: you should always think about one action to take. Only one action at a time in this format:
    Action:
    ```
    $JSON_BLOB
    ```
    Observation: the result of the action. This Observation is unique, complete, and the source of truth.
    ... (this Thought/Action/Observation can repeat N times, you should take several steps when needed. The $JSON_BLOB must be formatted as markdown and only use a SINGLE action at a time.)

    You must always end your output with the following format:

    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Now begin! Reminder to ALWAYS use the exact characters `Final Answer:` when you provide a definitive answer. """

    return (SYSTEM_PROMPT,)


@app.cell
def _(SYSTEM_PROMPT):
    # Since we are running the "text_generation", we need to add the right special tokens.
    prompt_01=f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    {SYSTEM_PROMPT}
    <|eot_id|><|start_header_id|>user<|end_header_id|>
    What's the weather in London ?
    <|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """
    return (prompt_01,)


@app.cell
def _(client, prompt_01):
    # Do you see the problem?
    client.text_generation(
        prompt_01,
        max_new_tokens=200,
    )
    return


@app.cell
def _(client, prompt_01):
    output = client.text_generation(
        prompt_01,
        max_new_tokens=200,
        stop=["Observation:"] # Let's stop before any actual function is called
    )
    return (output,)


@app.cell
def _():
    # Dummy function
    def get_weather(location):
        return f"the weather in {location} is sunny with low temperatures. \n"

    get_weather('London')

    return (get_weather,)


@app.cell
def _(get_weather, output, prompt):
    # Let's concatenate the base prompt, the completion until function execution and the result of the function as an Observation
    new_prompt=prompt+output+get_weather('London')
    print(new_prompt)
    return (new_prompt,)


@app.cell
def _(client, new_prompt):
    final_output = client.text_generation(
        new_prompt,
        max_new_tokens=200,
    )

    print(final_output)
    return (final_output,)


if __name__ == "__main__":
    app.run()
