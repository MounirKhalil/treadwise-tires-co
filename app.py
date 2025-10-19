"""
TreadWise Tire Co. - AI Business Agent
Deployment Script for Gradio/HuggingFace Spaces

Student: Mounir Khalil
ID: 202100437
"""

import os
import json
from datetime import datetime
from openai import OpenAI
import gradio as gr
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Load business summary
with open('me/Business_summary.txt', 'r') as f:
    business_summary = f.read()


# ============================================================================
# Tool Functions
# ============================================================================

def record_customer_interest(email: str, name: str, message: str) -> str:
    """
    Record customer interest by logging their contact information and message.

    Args:
        email: Customer's email address
        name: Customer's name
        message: Customer's message or inquiry

    Returns:
        Confirmation message
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create lead entry
    lead_entry = {
        "timestamp": timestamp,
        "name": name,
        "email": email,
        "message": message
    }

    # Log to file
    with open('customer_leads.jsonl', 'a') as f:
        f.write(json.dumps(lead_entry) + '\n')

    # Print for visibility
    print(f"\n{'='*60}")
    print("NEW CUSTOMER LEAD RECORDED")
    print(f"{'='*60}")
    print(f"Timestamp: {timestamp}")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Message: {message}")
    print(f"{'='*60}\n")

    return f"Thank you, {name}! Your information has been recorded. Our team will reach out to you at {email} shortly."


def record_feedback(question: str) -> str:
    """
    Record unanswered questions or feedback for improvement.

    Args:
        question: The question or feedback that couldn't be answered

    Returns:
        Confirmation message
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create feedback entry
    feedback_entry = {
        "timestamp": timestamp,
        "question": question
    }

    # Log to file
    with open('feedback_log.jsonl', 'a') as f:
        f.write(json.dumps(feedback_entry) + '\n')

    # Print for visibility
    print(f"\n{'='*60}")
    print("FEEDBACK/UNANSWERED QUESTION LOGGED")
    print(f"{'='*60}")
    print(f"Timestamp: {timestamp}")
    print(f"Question: {question}")
    print(f"{'='*60}\n")

    return "Question logged for review by our team."


# ============================================================================
# Tool Definitions for OpenAI
# ============================================================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "record_customer_interest",
            "description": "Record customer contact information when they want to learn more, schedule service, get a quote, or express interest in TreadWise services.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "Customer's email address"
                    },
                    "name": {
                        "type": "string",
                        "description": "Customer's full name"
                    },
                    "message": {
                        "type": "string",
                        "description": "Customer's inquiry, request, or message"
                    }
                },
                "required": ["email", "name", "message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "record_feedback",
            "description": "Log questions that you cannot answer or topics outside your knowledge base for team review.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question or topic you cannot answer"
                    }
                },
                "required": ["question"]
            }
        }
    }
]

# Map function names to actual functions
available_functions = {
    "record_customer_interest": record_customer_interest,
    "record_feedback": record_feedback
}


# ============================================================================
# System Prompt
# ============================================================================

system_prompt = f"""
You are a friendly and knowledgeable customer service agent for TreadWise Tire Co.

BUSINESS CONTEXT:
{business_summary}

YOUR ROLE:
- Answer questions about TreadWise's services, team, technology, and sustainability efforts
- Help customers understand our Smart Tread™ IoT monitoring platform
- Explain our mobile installation service and how it works
- Discuss our circular economy model (retreading, refurbishment, recycling)
- Provide information about our membership program and pricing
- Address fleet management and commercial tire solutions

GUIDELINES:
1. Stay in character as TreadWise's representative at all times
2. Be warm, professional, and solution-oriented
3. When customers express interest in services or want to learn more, collect their contact info using record_customer_interest
4. Encourage interested visitors to leave their contact details so our team can follow up
5. If you encounter a question you cannot answer from the business context, use record_feedback to log it
6. Focus on TreadWise's unique value: Smart Tread™ analytics, mobile service, sustainability, and transparent pricing
7. Be enthusiastic about our mission to make road travel safer and greener
8. Never make up information not provided in the business context

CONTACT COLLECTION:
When customers:
- Want to schedule a service
- Request a quote
- Ask about fleet solutions
- Express interest in membership
- Want more detailed information
→ Politely ask for their name, email, and details about their needs, then use record_customer_interest

Remember: You represent an innovative tire company that combines technology, convenience, and sustainability!
"""


# ============================================================================
# Chat Agent Implementation
# ============================================================================

def run_conversation(messages):
    """
    Run a conversation turn with the AI agent, handling tool calls if needed.

    Args:
        messages: List of conversation messages

    Returns:
        Assistant's response text
    """
    # First API call - get the assistant's response
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # If no tool calls, return the response
    if not tool_calls:
        return response_message.content

    # Handle tool calls
    messages.append(response_message)

    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        # Execute the function
        function_to_call = available_functions[function_name]
        function_response = function_to_call(**function_args)

        # Add tool response to messages
        messages.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": function_response
        })

    # Get final response after tool execution
    second_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return second_response.choices[0].message.content


# ============================================================================
# Gradio Chat Interface
# ============================================================================

# Initialize conversation history
conversation_history = [{"role": "system", "content": system_prompt}]

def chat_function(user_message, history):
    """
    Handle chat messages in Gradio interface.

    Args:
        user_message: User's input message
        history: Gradio chat history (not used, we maintain our own)

    Returns:
        Assistant's response
    """
    global conversation_history

    try:
        # Add user message to history
        conversation_history.append({"role": "user", "content": user_message})

        # Get assistant response
        assistant_response = run_conversation(conversation_history)

        # Ensure response is a string
        if assistant_response is None:
            assistant_response = "I apologize, but I encountered an issue. Please try again."

        assistant_response = str(assistant_response)

        # Add assistant response to history
        conversation_history.append({"role": "assistant", "content": assistant_response})

        return assistant_response

    except Exception as e:
        error_msg = f"I apologize, but I encountered an error: {str(e)}"
        print(f"Error in chat_function: {e}")
        return error_msg


# Create Gradio interface
demo = gr.ChatInterface(
    fn=chat_function,
    title="TreadWise Tire Co. - AI Assistant",
    description="Welcome to TreadWise! Ask me about our smart tire solutions, mobile installation, IoT monitoring, or sustainability programs. I'm here to help!",
    examples=[
        "What services does TreadWise offer?",
        "Tell me about the Smart Tread platform",
        "How does mobile installation work?",
        "What makes TreadWise different from other tire companies?",
        "Do you offer fleet management solutions?",
        "I'm interested in scheduling a tire installation"
    ]
)


# ============================================================================
# Launch Application
# ============================================================================

if __name__ == "__main__":
    demo.launch(share=True, debug=True)
