"""
Context Management Module for OpenAI Chat Sessions
Handles context size management to prevent token limit issues
"""

import tiktoken
import logging

# Initialize tokenizer for GPT-4
try:
  encoding = tiktoken.encoding_for_model("gpt-4o")
except KeyError:
  encoding = tiktoken.get_encoding("cl100k_base")


def count_tokens(messages):
  """Count tokens in message list"""
  total_tokens = 0
  for message in messages:
    # Count tokens for role and content
    total_tokens += len(encoding.encode(str(message.get("role", ""))))
    total_tokens += len(encoding.encode(str(message.get("content", ""))))

    # Count tokens for tool calls if present
    if message.get("tool_calls"):
      total_tokens += len(encoding.encode(str(message["tool_calls"])))

  return total_tokens


def truncate_context(messages, max_tokens=8000):
  """
  Strategy 1: Simple truncation - keep system message and recent messages
  """
  if not messages:
    return messages

  # Always keep system message
  system_message = messages[0] if messages[0]["role"] == "system" else None
  recent_messages = messages[1:] if system_message else messages

  # Calculate tokens and truncate from the beginning
  while count_tokens([system_message] + recent_messages if system_message else recent_messages) > max_tokens and len(recent_messages) > 1:
    recent_messages = recent_messages[1:]  # Remove oldest non-system message

  return ([system_message] + recent_messages) if system_message else recent_messages


def smart_context_compression(messages, max_tokens=8000):
  """
  Strategy 2: Smart compression - keep system, recent messages, and important context
  """
  if not messages or count_tokens(messages) <= max_tokens:
    return messages

  # Separate message types
  system_messages = [msg for msg in messages if msg["role"] == "system"]

  # Always keep system messages
  essential_messages = system_messages.copy()

  # Keep last N user-assistant pairs
  recent_pairs = []
  i = len(messages) - 1
  pairs_kept = 0
  max_pairs = 5  # Adjust based on needs

  while i >= 0 and pairs_kept < max_pairs:
    if messages[i]["role"] in ["user", "assistant", "tool"]:
      recent_pairs.insert(0, messages[i])
      if messages[i]["role"] == "user":
        pairs_kept += 1
    i -= 1

  compressed_messages = essential_messages + recent_pairs

  # Final truncation if still too long
  return truncate_context(compressed_messages, max_tokens)


def summarize_old_context(messages, max_tokens=8000):
  """
  Strategy 3: Summarization - create summary of old context
  """
  if not messages or count_tokens(messages) <= max_tokens:
    return messages

  system_message = messages[0] if messages[0]["role"] == "system" else None
  conversation_messages = messages[1:] if system_message else messages

  # Keep recent messages (last 100)
  recent_messages = conversation_messages[-100:] if len(conversation_messages) > 100 else conversation_messages
  old_messages = conversation_messages[:-100] if len(conversation_messages) > 100 else []

  if old_messages and count_tokens([system_message] + recent_messages if system_message else recent_messages) > max_tokens * 0.7:
    # Create summary of old messages
    summary_content = "Previous conversation summary:\n"

    # Extract key information from old messages
    for msg in old_messages:
      if msg["role"] == "user":
        summary_content += f"User asked about: {msg['content'][:100]}...\n"
      elif msg["role"] == "assistant" and not msg.get("tool_calls"):
        summary_content += f"Assistant provided info about hotels/travel.\n"

    summary_message = {
      "role": "system",
      "content": summary_content
    }

    result = [system_message, summary_message] + recent_messages if system_message else [summary_message] + recent_messages
    return truncate_context(result, max_tokens)

  return ([system_message] + recent_messages) if system_message else recent_messages


def clean_tool_messages(messages):
  """
  Strategy 4: Remove old tool call/response pairs while keeping recent ones
  """
  if not messages:
    return messages

  cleaned = []
  recent_tool_window = 20  # Keep last 20 messages for tool context

  for i, message in enumerate(messages):
    # Always keep system messages
    if message["role"] == "system":
      cleaned.append(message)
      continue

    # Keep recent messages (including tool calls)
    if i >= len(messages) - recent_tool_window:
      cleaned.append(message)
      continue

    # For older messages, only keep user and assistant (non-tool) messages
    if message["role"] in ["user", "assistant"] and not message.get("tool_calls"):
      cleaned.append(message)

  return cleaned


def manage_context(messages, strategy="smart_compression", max_tokens=8000):
  """
  Main context management function

  Args:
      messages: List of conversation messages
      strategy: Context management strategy to use
      max_tokens: Maximum token limit

  Returns:
      Processed messages list
  """
  current_tokens = count_tokens(messages)

  # Log context stats
  logging.info(f"Context management: {len(messages)} messages, {current_tokens} tokens, strategy: {strategy}")

  if current_tokens <= max_tokens:
    return messages

  if strategy == "truncate":
    result = truncate_context(messages, max_tokens)
  elif strategy == "smart_compression":
    result = smart_context_compression(messages, max_tokens)
  elif strategy == "summarize":
    result = summarize_old_context(messages, max_tokens)
  elif strategy == "clean_tools":
    result = clean_tool_messages(messages)
    result = truncate_context(result, max_tokens)
  else:
    # Default to smart compression
    result = smart_context_compression(messages, max_tokens)

  new_tokens = count_tokens(result)
  logging.info(f"Context reduced: {len(messages)} -> {len(result)} messages, {current_tokens} -> {new_tokens} tokens")

  return result


def cleanup_old_conversations(session_store, max_conversations=100):
  """
  Remove oldest conversations if session store gets too large

  Args:
      session_store: Dictionary containing all conversations
      max_conversations: Maximum number of conversations to keep
  """
  if len(session_store) > max_conversations:
    # Sort by conversation_id and remove oldest (assuming timestamp-based IDs)
    sorted_ids = sorted(session_store.keys())
    to_remove = sorted_ids[:-max_conversations]

    for conv_id in to_remove:
      del session_store[conv_id]

    logging.info(f"Cleaned up {len(to_remove)} old conversations")