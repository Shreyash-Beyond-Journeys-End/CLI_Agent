import subprocess , asyncio , os , requests , inspect

from dotenv import load_dotenv

from huggingface_hub import AsyncInferenceClient

from models import SafetyStatus , LlmResponse , ApplicationStyles

from langchain_core.output_parsers import PydanticOutputParser

from prompts import getSecuritySysPrompt , getMainLLmPrompt

from bs4 import BeautifulSoup

from rich.console import Console





load_dotenv()

client = AsyncInferenceClient(
    model = os.getenv("huggingface_model_id"),
    api_key = os.getenv("hugging_face_key")
    
)

console = Console()

app_styles = ApplicationStyles()

def write_file(filepath: str, content: str) -> str:


    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return f"Successfully wrote code to {filepath}"


async def callLLM(messages: list):

    response = await client.chat_completion(
        messages=messages,
    )

    return response.choices[0].message.content



async def executeCommandTool(command: str) -> str:

    parser = PydanticOutputParser(pydantic_object=SafetyStatus)

    sys_prompt = getSecuritySysPrompt(parser.get_format_instructions())


    messages = [
        {"role":"system" , "content" : sys_prompt},
        {"role" : "user" , "content" : f"agent wants to run: {command}"}
    ]

    response = await callLLM(messages)

    safety_result = parser.invoke(response)


    if(safety_result.safe == False):

        return f"Execution Failed. Contains dangerous command . Reason : {safety_result.reason}"


    result = subprocess.run(command , shell=True , capture_output=True , text=True) 


    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Execution Failed : {result.stderr.strip()}"



def get_website_html(url: str):
    html = requests.get(url).text
    soup = BeautifulSoup(html , 'html.parser')
   
    for tag in soup(["script", "style", "svg", "noscript", "img", "iframe", "path", "meta", "link"]):
        tag.decompose()
        
    clean_html = soup.prettify()
    

        
    return clean_html



tool_map = {
    "get_website_html" : get_website_html,
    "executeCommandTool" : executeCommandTool,
    "write_file" : write_file  
}


async def handel_user_request(user_input):
    
    parser = PydanticOutputParser(pydantic_object=LlmResponse)

    sys_prompt = getMainLLmPrompt(parser.get_format_instructions())
    
    messages = [
        {"role" : "system" , "content" : sys_prompt},
        {"role" : "user" , "content" : user_input}
    ]


    while(True):
        print("\n")

        raw_response = await callLLM(messages)

        response = parser.invoke(raw_response)



        messages.append(
            {"role" : "assistant" , "content" : raw_response}
        )



        if response.step == "START":
            console.print("STARTING STEP .... " , style=app_styles.step)

            console.print(response.content , style=app_styles.content)

            messages.append({"role": "user", "content": "Please continue to the next step."})

        elif response.step == "THINK":
            console.print("THINKING ..... ", style=app_styles.step)

            console.print(response.content , style=app_styles.content)

            messages.append({"role": "user", "content": "Please continue to the next step."})

        elif response.step == "TOOL":

            console.print("TOOL calling .... " , style=app_styles.step)

            console.print(f"Calling {response.tool_name}" , style=app_styles.tool)

            tool = tool_map.get(response.tool_name)

            if tool :
                if inspect.iscoroutinefunction(tool):
                    result = await tool(*response.tool_args)
                else:
                    result = tool(*response.tool_args)
            else :
                result = f"this {response.tool_name} toll is not available"

            content = {
                "step" : "OBSERVE",
                "content" : result,
                "tool": None,
                "tool_args": []
            }


            messages.append(
                {"role" : "user" , "content" : LlmResponse(step="OBSERVE", content=str(result), tool_name=None).model_dump_json()}
            )


        elif response.step == "OUTPUT":
            console.print("OUTPUT" , style=app_styles.step)

            console.print(response.content , style=app_styles.output)

            break




async def RunApllication():

    print("Hello how can I assist you today")
    while(True):
        print("\n")
        user_input = input("Message: ")


        if(user_input=="exit"):
            break

        await handel_user_request(user_input)



asyncio.run(RunApllication())
