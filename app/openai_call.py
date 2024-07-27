from openai import OpenAI
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = OpenAI()

def api_call(last_year_data, current_year_data):
    logger.info("Starting API call...")
    try:
        thread = client.beta.threads.create()
        logger.info(f"Created thread with ID: {thread.id}")
        
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content= f"Schreibe einen Bericht über die performance meiner Website und vergleiche die Daten vom letztem Zeitraum mit den aktuellen Daten. Analysiere die Daten gründlich und vollständig. Daten des letzten Zeitraums: {last_year_data}. Daten diesen Zeitraums:{current_year_data}."
        )
        logger.info(f"Created message with ID: {message.id}")
        
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id="asst_vn052cslMtYMkq2wRwP2g7JO",
        )
        logger.info(f"Run status: {run.status}")
        
        if run.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            logger.info(f"Retrieved {len(messages.data)} messages")
            if messages.data:
                content = messages.data[0].content
                if content and len(content) > 0 and hasattr(content[0], 'text'):
                    return content[0].text.value
                else:
                    logger.warning("No text content found in the message")
                    return "No analysis generated."
            else:
                logger.warning("No messages retrieved from the thread")
                return "No analysis generated."
        else:
            logger.warning(f"Run did not complete. Status: {run.status}")
            return "API call did not complete successfully."
    except Exception as e:
        logger.error(f"Error in API call: {str(e)}", exc_info=True)
        return f"Error occurred during API call: {str(e)}"

