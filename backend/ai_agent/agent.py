import asyncio
import os
import uuid
from dotenv import load_dotenv
from agents import Agent, Runner
from agents.mcp import MCPServerSse
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
MCP_URL = "http://localhost:8080"
SESSION_TOKEN = os.getenv("SESSION_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- Initialize OpenAI Client ---
client = OpenAI(api_key=OPENAI_API_KEY)


class TodoAgent(Agent):
    """
    An Agent that uses an OpenAI model and tools from an MCP server.
    """
    def __init__(self, mcp_server: MCPServerSse):
        super().__init__(
            client=client,
            model="gpt-4o-mini",
            mcp_servers=[mcp_server],
            system_prompt="You are a helpful task management assistant. Your goal is to help users manage their todo tasks by calling the available functions.",
        )


async def main():
    """
    The main asynchronous function to run the agent chat loop.
    """
    if not OPENAI_API_KEY:
        print("ERROR: OPENAI_API_KEY environment variable not set.")
        return

    mcp_server = MCPServerSse({"url": MCP_URL})

    try:
        print("Connecting to MCP server...")
        await mcp_server.connect()
        mcp_tools = await mcp_server.get_tools()
        print(f"✅ Successfully loaded {len(mcp_tools)} tools from the MCP server.")

        # --- Initialize Agent and Runner ---
        agent = TodoAgent(mcp_server=mcp_server)
        
        session_id = SESSION_TOKEN or str(uuid.uuid4())
        print(f"Using session ID: {session_id}")
        
        runner = Runner(agent=agent, session_id=session_id)

        # --- Start Chat Loop ---
        print("\n🤖 AI Task Assistant is ready (type 'exit' to quit)")
        print("-" * 50)

        while True:
            try:
                user_input = await asyncio.to_thread(input, "\nYou: ")
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                break

            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            if not user_input.strip():
                continue

            print("\nAssistant:", end="", flush=True)
            try:
                final_response = None
                async for chunk in runner.run(user_input):
                    if chunk.type == 'content' and isinstance(chunk.data, str):
                        print(chunk.data, end="", flush=True)
                    if chunk.type == 'final':
                        final_response = chunk.data
                
                # If the final response wasn't printed as content chunks
                if final_response and not isinstance(final_response, str) :
                     print(final_response, end="")

                print() # Newline after assistant's full response

            except Exception as e:
                print(f"\nAn error occurred: {e}")

    except Exception as e:
        print(f"❌ Failed to connect to MCP server at {MCP_URL}. Please ensure it is running.")
        print(f"Error: {e}")
    finally:
        if mcp_server:
            await mcp_server.cleanup()
            print("\nMCP server connection closed.")


if __name__ == "__main__":
    asyncio.run(main())
