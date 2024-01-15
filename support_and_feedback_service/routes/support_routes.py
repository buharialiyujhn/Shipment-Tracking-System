# routes/support_routes.py

from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from app import SupportTicket  # Adjust as per your model structure
from app import Feedback  # Adjust as per your model structure
from extensions import db
from sqlalchemy.exc import SQLAlchemyError

support_bp = Blueprint('support_bp', __name__)


@support_bp.route('/ticket', methods=['GET', 'POST'])
def create_support_ticket():
    if request.method == 'POST':
        data = request.form
        content = data.get('content')

        if not content:
            return render_template('create_ticket.html', error='Content is missing')

        new_support_ticket = SupportTicket(content=content)
        db.session.add(new_support_ticket)
        db.session.commit()

        return redirect(url_for('support_bp.list_tickets'))

    return render_template('create_ticket.html')


@support_bp.route('/tickets', methods=['GET'])
def list_tickets():
    tickets = SupportTicket.query.all()
    return render_template('list_tickets.html', tickets=tickets)


@support_bp.route('/tickets/<int:ticket_id>', methods=['GET'])
def view_ticket(ticket_id):
    ticket = SupportTicket.query.get_or_404(ticket_id)
    return render_template('view_ticket.html', ticket=ticket)


@support_bp.route('/tickets/<int:ticket_id>', methods=['PUT', 'PATCH'])
def update_ticket(ticket_id):
    # Implement logic to update the ticket
    ticket = SupportTicket.query.get_or_404(ticket_id)
    # Update ticket details here
    return jsonify({'message': 'Ticket updated successfully', 'ticket_id': ticket_id}), 200


@support_bp.route('/tickets/<int:ticket_id>/close', methods=['PUT', 'PATCH'])
def close_ticket(ticket_id):
    # Implement logic to close the ticket
    ticket = SupportTicket.query.get_or_404(ticket_id)
    ticket.status = 'closed'
    db.session.commit()
    return jsonify({'message': 'Ticket closed successfully', 'ticket_id': ticket_id}), 200


@support_bp.route('/feedback', methods=['GET', 'POST'])
def submit_feedback():
    if request.method == 'POST':
        data = request.form
        user_feedback = data.get('feedback')
        user_id = data.get('user_id')  # Assuming feedback is linked to a user

        if not user_feedback or not user_id:
            return render_template('submit_feedback.html', error='Feedback or user ID is missing')

        try:
            feedback = Feedback(user_id=user_id, feedback=user_feedback)
            db.session.add(feedback)
            db.session.commit()
            return redirect(url_for('support_bp.list_feedback'))
        except SQLAlchemyError as e:
            return render_template('submit_feedback.html', error=str(e))

    return render_template('submit_feedback.html')


@support_bp.route('/feedback/list', methods=['GET'])
def list_feedback():
    feedbacks = Feedback.query.all()
    return render_template('list_feedback.html', feedbacks=feedbacks)


# Additional routes can be added as per requirements
# Add more routes as needed for other endpoints like viewing feedback, generating reports, etc.

# routes/support_routes.py continued


@support_bp.route('/feedback/<int:feedback_id>', methods=['GET'])
def view_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    return render_template('view_feedback.html', feedback=feedback)


@support_bp.route('/feedback/reports', methods=['GET'])
def generate_feedback_report():
    report = "Generated report data based on feedback"
    return render_template('feedback_report.html', report=report)


@support_bp.route('/tickets/reports', methods=['GET'])
def generate_ticket_report():
    report = "Generated report data based on support tickets"
    return render_template('ticket_report.html', report=report)


@support_bp.route('/analytics/dashboard', methods=['GET'])
def view_dashboard():
    # Logic to display analytics on a dashboard
    # Placeholder for dashboard data
    dashboard_data = "Dashboard analytics data"
    return render_template('dashboard.html', data=dashboard_data)

# Additional endpoints can be added here as per future requirements
