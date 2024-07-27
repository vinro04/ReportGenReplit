from flask import render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_user, login_required, logout_user, current_user
from app import app
from app.models import User, get_user
from app.reports import generate_yoy_report, generate_monthly_report
from datetime import datetime
import logging
import io
import uuid

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add the accounts dictionary
accounts = {
    "Medialab": 250074345,
    "Praxis Radolfzell": 324096036,
    "Alexandra Mogilevskaia": 416374293,
    "Deine3a": 294659732,
    "Trenzyme.com": 316721341,
    "Inlingua DE": 327839759,
    "Inlingua München": 323055093
}

# Dictionary to store reports
reports = {}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user(username)
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html', accounts=accounts)

@app.route('/generate_report', methods=['POST'])
@login_required
def generate_report():
    try:
        logger.debug("Received request to generate report")
        data = request.json
        logger.debug(f"Request data: {data}")
        
        property_id = data['property_id']
        report_type = data['report_type']
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')

        logger.debug(f"Generating {report_type} report for property {property_id}")
        
        if report_type == 'yoy':
            report = generate_yoy_report(property_id, start_date, end_date)
        elif report_type == 'monthly':
            report = generate_monthly_report(property_id, start_date, end_date)
        else:
            logger.error(f"Invalid report type: {report_type}")
            return jsonify({'error': 'Invalid report type'}), 400

        # Generate a unique ID for this report
        report_id = str(uuid.uuid4())
        
        # Store the report in the dictionary
        reports[report_id] = report
        logger.debug(f"Report generated and stored with ID: {report_id}")

        return jsonify({'report_id': report_id})
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/download_report/<report_id>')
@login_required
def download_report(report_id):
    try:
        logger.debug(f"Received request to download report with ID: {report_id}")
        report = reports.get(report_id)
        if not report:
            logger.error(f"No report found for ID: {report_id}")
            return jsonify({'error': 'No report found. Please generate a report first.'}), 404

        # Create a BytesIO object
        report_io = io.BytesIO()
        report_io.write(report.encode('utf-8'))
        report_io.seek(0)

        # Remove the report from the dictionary after sending
        reports.pop(report_id, None)
        logger.debug(f"Report {report_id} sent and removed from storage")

        return send_file(
            report_io,
            as_attachment=True,
            download_name='analytics_report.txt',
            mimetype='text/plain'
        )
    except Exception as e:
        logger.error(f"Error downloading report: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

# Add this line to help debug
@app.route('/debug')
@login_required
def debug():
    logger.debug("Debug route accessed")
    return jsonify({
        "message": "Debug route is working!",
        "reports_in_memory": len(reports),
        "report_ids": list(reports.keys())
    })