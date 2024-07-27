from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_data(property_id, start_date, end_date):
    client = BetaAnalyticsDataClient()
    # Convert datetime objects to string in YYYY-MM-DD format
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    reports = {
        "overall": run_report_overall,
        "browser": run_report_browser,
        "city": run_report_city,
        "page_url": run_report_upage_url,
        "user_source": run_report_user_source,
        "events": run_report_ereignisse,
        "conversion_origin": run_report_conversion_herkunft,
        "devices": run_report_geräte
    }
    
    data = {}
    with ThreadPoolExecutor(max_workers=len(reports)) as executor:
        future_to_report = {executor.submit(report_func, client, property_id, start_date_str, end_date_str): report_name 
                            for report_name, report_func in reports.items()}
        for future in as_completed(future_to_report):
            report_name = future_to_report[future]
            try:
                data[report_name] = future.result()
            except Exception as e:
                raise Exception(f"Error in {report_name} report: {str(e)}")
    
    return {
        "Zeitraum": {"Anfang": start_date_str, "Ende": end_date_str},
        "Kennzahlen": data.get("overall", {}),
        "Zielgruppe": {"Browser": data.get("browser", {}), "Geräte": data.get("devices", {})},
        "Besucher Quellen": data.get("user_source", {}),
        "Top Städte": data.get("city", {}),
        "Conversions und Ereignisse": data.get("events", {}),
        "Herkunft der Conversions ": data.get("conversion_origin", {}),
        "Top Seiten": data.get("page_url", {})
    }

def run_report_overall(client, property_id, start_date, end_date):
    try:
        request = RunReportRequest(
            property=f"properties/{property_id}",
            metrics=[
                Metric(name="newUsers"),
                Metric(name="totalUsers"),
                Metric(name="sessions"),
                Metric(name="screenPageViews"),
                Metric(name="engagementRate"),
                Metric(name="screenPageViewsPerUser"),
                Metric(name="userEngagementDuration")
            ],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        )
        response = client.run_report(request)
        return format_response(response)
    except Exception as e:
        raise Exception(f"Error in run_report_overall: {str(e)}")

def run_report_browser(client, property_id, start_date, end_date):
    try:
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="browser")],
            metrics=[
                Metric(name="newUsers"),
                Metric(name="totalUsers"),
                Metric(name="conversions"),
                Metric(name="engagementRate"),
                Metric(name="userEngagementDuration")
            ],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        )
        response = client.run_report(request)
        return format_response(response)
    except Exception as e:
        raise Exception(f"Error in run_report_browser: {str(e)}")

def run_report_city(client, property_id, start_date, end_date):
    try:
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="city")],
            metrics=[
                Metric(name="newUsers"),
                Metric(name="totalUsers"),
                Metric(name="sessions"),
                Metric(name="engagementRate"),
                Metric(name="userEngagementDuration"),
                Metric(name="eventCountPerUser")
            ],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        )
        response = client.run_report(request)
        return format_response(response)
    except Exception as e:
        raise Exception(f"Error in run_report_city: {str(e)}")

def run_report_upage_url(client, property_id, start_date, end_date):
    try:
        if not isinstance(property_id, str):
            property_id = str(property_id)
        
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="fullPageUrl")],
            metrics=[
                Metric(name="newUsers"),
                Metric(name="totalUsers"),
                Metric(name="screenPageViews"),
                Metric(name="userEngagementDuration")
            ],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        )
        response = client.run_report(request)
        return format_response(response)
    except Exception as e:
        raise Exception(f"Error in run_report_upage_url: {str(e)}, Types: property_id: {type(property_id)}, start_date: {type(start_date)}, end_date: {type(end_date)}")


def run_report_user_source(client, property_id, start_date, end_date):
    try:
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="firstUserSource"), Dimension(name="firstUserMedium")],
            metrics=[
                Metric(name="totalUsers"),
                Metric(name="newUsers"),
                Metric(name="sessions"),
                Metric(name="userEngagementDuration"),
                Metric(name="engagementRate"),
                Metric(name="conversions")
            ],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        )
        response = client.run_report(request)
        return format_response(response)
    except Exception as e:
        raise Exception(f"Error in run_report_user_source: {str(e)}")

def run_report_ereignisse(client, property_id, start_date, end_date):
    try:
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="eventName")],
            metrics=[
                Metric(name="conversions")
            ],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        )
        response = client.run_report(request)
        return format_response(response)
    except Exception as e:
        raise Exception(f"Error in run_report_ereignisse: {str(e)}")

def run_report_conversion_herkunft(client, property_id, start_date, end_date):
    try:
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="eventName"), Dimension(name="city")],
            metrics=[
                Metric(name="conversions")
            ],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        )
        response = client.run_report(request)
        return format_response(response)
    except Exception as e:
        raise Exception(f"Error in run_report_conversion_herkunft: {str(e)}")

def run_report_geräte(client, property_id, start_date, end_date):
    try:
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="deviceCategory")],
            metrics=[
                Metric(name="totalUsers")
            ],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        )
        response = client.run_report(request)
        return format_response(response)
    except Exception as e:
        raise Exception(f"Error in run_report_geräte: {str(e)}")

def format_response(response):
    try:
        return {
            "metricHeaders": [header.name for header in response.metric_headers],
            "rows": [{"dimensionValues": [str(value.value) for value in row.dimension_values], 
                      "metricValues": [str(value.value) for value in row.metric_values]} 
                     for row in response.rows[:10]]  # Limit to top 10 rows
        }
    except Exception as e:
        raise Exception(f"Error in format_response: {str(e)}")