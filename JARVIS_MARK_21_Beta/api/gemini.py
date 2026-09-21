from dotenv import load_dotenv
import os
from core.agent_tools import AGENT_TOOLS, execute_tool_call

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    genai = None
    GENAI_AVAILABLE = False

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

model = None
if GENAI_AVAILABLE and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash", tools=AGENT_TOOLS)
    except Exception as e:
        print(f"⚠️ Warning initializing Gemini model with tools: {e}")
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
        except Exception:
            model = None


def generate_agentic_response(prompt: str) -> str:
    """Send prompt to Gemini with automatic or manual function calling agent loop."""
    if not GENAI_AVAILABLE:
        return "Google Generative AI SDK is not installed. Please run 'pip install google-generativeai'."
    if not GEMINI_API_KEY:
        return "Gemini API key is not configured. Please set GEMINI_API_KEY in your .env file."
    
    try:
        # Start chat with automatic function calling enabled if supported
        chat = model.start_chat(enable_automatic_function_calling=True)
        response = chat.send_message(prompt)
        
        # Check if function calls were returned manually (if auto-call is off or partial)
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "function_call") and part.function_call:
                    fn_name = part.function_call.name
                    fn_args = dict(part.function_call.args)
                    print(f"🤖 Gemini Tool Invoked: {fn_name}({fn_args})")
                    tool_result = execute_tool_call(fn_name, fn_args)
                    
                    # Send tool result back to Gemini for final response synthesis
                    response = chat.send_message(
                        genai.types.Content(
                            parts=[
                                genai.types.Part.from_function_response(
                                    name=fn_name,
                                    response={"result": tool_result}
                                )
                            ]
                        )
                    )
                    break
        
        return response.text.strip() if response.text else "Done."
    except Exception as e:
        print(f"⚠️ Agentic Gemini Error: {e}")
        # Fallback to direct model generation if chat session encounters an error
        try:
            fallback_model = genai.GenerativeModel("gemini-2.0-flash")
            res = fallback_model.generate_content(prompt)
            return res.text.strip()
        except Exception as err:
            return f"Sorry, I couldn't process your request: {err}"
