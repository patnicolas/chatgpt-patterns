# chatgpt-patterns
*Patrick Nicolas last update 06.07.2023*

The objective is this framework is to evaluate and extended Prompt engineering techniques to build applications. These techniques include
- Prompt patterns: *Output automater*, *Persona*, *Fact checking template* and *cognitive verifier*
- Typed workflow using **langchain**

## References 
- [ChatGPT Prompt patterns for code generation](http://patricknicolas.blogspot.com/2023/05/chatgpt-prompt-patterns-for-code.html)
- [LangChain introduction](https://python.langchain.com/en/latest/index.html)
- [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/pdf/2201.11903.pdf)
- [OpenAI ChatGPT](https://openai.com/chatgpt)


## Environment
| Package      | Version |
|:-------------|:--------|
| python       | 3.9.16  |
| torch        | 2.0.1   |
| openai       | 0.27.1  |
| matplotlib   | 3.7.1   |
| scikit-learn | 1.2.2   |
| numpy        | 1.24.3  |
| pandas       | 2.0.2   |
| langchain    | 0.0.197 |
| polars       | 0.17.0  |
| fastapi      | 0.97.0  |


## Updates
| Date       | Version |
|:-----------|:--------|
| 06.07.2023 | 0.1     |
| 06.18.2023 | 0.2     |


## Packages
|Package|Description|
|:--|:--|
|util|Utilities class|
|chatgpt|Classes related to usage and fine tuning for ChatGPT|
|web|Web service and UI|


## Prompt patterns
From the seminal paper "A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT".

| Name    | Overview                                                                                                                                                              | Contextual statements                                                                                                                                                           |
|:--------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Persona | **Output customization**<br>Assign a persona, role or domain expert to LLM. The persona can be expressed as a role, job description, title, historical or known figure.| - I would like you to ask me questions to achieve X.<br>- You should ask questions until X is achieved or the condition X is met. Ask me questions regarding X one at the time. | 
| Template | **Output customization**<br>Ensure output follows a precise template (i.e. format, URL, example…). This pattern instructs LLM to use a unique format in specific portion of the answer.|I am going to provide you with a template for your output<br>X is my place holder for content<br>Try to fit the output into one or more of the placeholders that I listed<br>Please preserve the formatting and template I provided<br>Here is the template to follow: PATTERN with PLACEHOLDER.<br>|
|Fact check list|**Error identification**<br>Request LLM to provide/append a list of facts/assumptions to the answer, so the user may perform due-diligence.|Generate a set of facts that are contained in the output<br>The set of facts should be inserted/appended to the output<br>The set of facts should be the fundamental facts that could undermine the veracity of the output if any of them are incorrect.|
|Reflection|**Error identification**<br>Ask LLM to automatically explain the rationale behind a given answers to the user. The pattern clarifies any points of confusion, underlying assumptions, gaps in knowledge….|Whenever you generate an answer, explain the reasoning and assumptions behind your answer, so I can improve my question.|
|Output automater|**Output customization**<br>Having LLM generate a script or automated task that can be execute any steps the LLM recommends.|Whenever you produce an output with steps, always do this. Produce an executable artifact of type X that will automate these steps.|
|Visualization Generator|**Output customization**<br>Use generated text to create a visualization as complex concepts are easier to grasp with diagrams and images. The LLM output should create a pathway for the tool to produce imagery.|Generate an X that I can provide to tool Y to visualize it.|

