"""
Runner for the Gemini Agent
Manages conversations and interactions with the Gemini AI assistant
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import json
from sqlmodel import Session

from .gemini_agent import gemini_todo_agent
from ..mcp.server import mcp_server

load_dotenv()

class GeminiAgentRunner:
    def __init__(self):
        self.agent = gemini_todo_agent

    async def process_conversation(self, user_message: str, session: Session, user_id: str = None):
        """
        Process a complete conversation turn with Gemini
        """
        try:
            # Prepare the conversation message
            messages = [
                {
                    "role": "user",
                    "content": user_message
                }
            ]

            # Get response from Gemini
            response = self.agent.run_gemini_conversation(messages)

            # Check if the response contains function calls (tool calls)
            # The response object from Gemini has a specific structure for function calls
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                        for part in candidate.content.parts:
                            # Check if this part is a function call
                            if hasattr(part, 'function_call') and part.function_call:
                                # Process function call
                                function_call = part.function_call

                                # Extract function name and arguments
                                func_name = function_call.name
                                args_dict = {}

                                # Extract arguments from the function call
                                if hasattr(function_call, 'args'):
                                    # Convert args to dict
                                    args_str = str(function_call.args)
                                    # For now, we'll handle this as a basic conversion
                                    # In practice, args should be parsed properly

                                    # Execute the tool using the MCP server
                                    tool_result = await mcp_server.execute_tool(
                                        tool_name=func_name,
                                        session=session,
                                        user_id=user_id,
                                        **function_call.args  # Pass the arguments directly
                                    )

                                    # Format the tool result for the AI
                                    if tool_result["success"]:
                                        # For now, return a basic response
                                        return {
                                            "response": f"Operation completed successfully: {func_name}",
                                            "tool_calls": [func_name],
                                            "tool_results": [tool_result["result"]]
                                        }
                                    else:
                                        return {
                                            "response": f"Error executing {func_name}: {tool_result['error']}",
                                            "tool_calls": [func_name],
                                            "tool_results": [tool_result["error"]]
                                        }

            # If no function calls were made, return the text response
            if hasattr(response, 'text'):
                return {
                    "response": response.text,
                    "tool_calls": [],
                    "tool_results": []
                }
            elif hasattr(response, '_result') and hasattr(response._result, 'candidates'):
                # Alternative way to access the text if it's in _result
                candidates = response._result.candidates
                for candidate in candidates:
                    if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                        text_parts = []
                        for part in candidate.content.parts:
                            if hasattr(part, 'text') and part.text:
                                text_parts.append(part.text)
                        if text_parts:
                            return {
                                "response": " ".join(text_parts),
                                "tool_calls": [],
                                "tool_results": []
                            }

            # Fallback response
            return {
                "response": f"I processed your message: '{user_message}'. The system is now using Google Gemini API.",
                "tool_calls": [],
                "tool_results": []
            }
        except Exception as e:
            print(f"Error processing conversation with Gemini: {str(e)}")
            return {
                "response": f"Error processing your request: {str(e)}",
                "tool_calls": [],
                "tool_results": []
            }

# Global instance
gemini_agent_runner = GeminiAgentRunner()