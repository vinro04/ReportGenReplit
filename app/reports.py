import logging
from app.data_fetcher import fetch_data
from datetime import timedelta

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    from app.openai_call import api_call
    logger.info("Successfully imported api_call from app.openai_call")
except ImportError:
    logger.warning("Could not import api_call function. OpenAI integration will not be available.")
    api_call = None

def generate_yoy_report(property_id, start_date, end_date):
    try:
        property_id = str(property_id)  # Ensure property_id is a string
        current_year_data = fetch_data(property_id, start_date, end_date)

        last_year_start = start_date - timedelta(days=365)
        last_year_end = end_date - timedelta(days=365)
        last_year_data = fetch_data(property_id, last_year_start, last_year_end)

        report = f"Monatlicher Report (Jahresvergleich) für den Zeitraum: {start_date.strftime('%Y-%m-%d')} bis {end_date.strftime('%Y-%m-%d')}\n\n"

        # Call the OpenAI API if available
        if api_call:
            logger.info("Calling OpenAI API...")
            try:
                ai_generated_report = api_call(last_year_data, current_year_data)
                logger.info(f"AI generated report: {ai_generated_report}")
                if ai_generated_report:
                    report += f"AI Analysis:\n{ai_generated_report}\n\n"
                else:
                    logger.warning("AI-generated report is empty")
                    report += "AI Analysis: No analysis generated.\n\n"
            except Exception as e:
                logger.error(f"Error occurred during API call: {e}")
                report += f"AI Analysis: An error occurred during the API call: {str(e)}\n\n"
        else:
            logger.warning("API call function not available")
            report += "AI Analysis: Not available due to integration issues.\n\n"

        logger.info(f"Final report: {report}")
        return report

    except Exception as e:
        logger.error(f"Error in generate_yoy_report: {str(e)}", exc_info=True)
        raise

def generate_monthly_report(property_id, start_date, end_date):
    try:
        property_id = str(property_id)  # Ensure property_id is a string
        current_month_data = fetch_data(property_id, start_date, end_date)

        last_month_start = start_date - timedelta(days=30)  # Approximate
        last_month_end = end_date - timedelta(days=30)
        last_month_data = fetch_data(property_id, last_month_start, last_month_end)

        report = f"Monatlicher Report (Monatsvergleich) für den Zeitraum: {start_date.strftime('%Y-%m-%d')} bis {end_date.strftime('%Y-%m-%d')}\n\n"

        # Call the OpenAI API if available
        if api_call:
            logger.info("Calling OpenAI API...")
            try:
                ai_generated_report = api_call(last_month_data, current_month_data)
                logger.info(f"AI generated report: {ai_generated_report}")
                if ai_generated_report:
                    report += f"AI Analysis:\n{ai_generated_report}\n\n"
                else:
                    logger.warning("AI-generated report is empty")
                    report += "AI Analysis: No analysis generated.\n\n"
            except Exception as e:
                logger.error(f"Error occurred during API call: {e}")
                report += f"AI Analysis: An error occurred during the API call: {str(e)}\n\n"
        else:
            logger.warning("API call function not available")
            report += "AI Analysis: Not available due to integration issues.\n\n"

        logger.info(f"Final report: {report}")
        return report

    except Exception as e:
        logger.error(f"Error in generate_monthly_report: {str(e)}", exc_info=True)
        raise