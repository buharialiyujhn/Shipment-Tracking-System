from datetime import datetime

import web3
from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.shipment import db, Shipment
from web3 import Web3, HTTPProvider
import os
import json

from web3.exceptions import TimeExhausted

shipment_bp = Blueprint('shipment_bp', __name__)


@shipment_bp.route('/create', methods=['GET', 'POST'])
def create_shipment():
    if request.method == 'POST':
        # Extract data from the request
        tracking_number = request.form.get('trackingNumber')
        status = request.form.get('status')
        amount = request.form.get('amount', type=float)
        is_paid = request.form.get('isPaid', type=bool) # Assuming 'isPaid' is sent as a boolean
        transaction_hash = request.form.get('transactionHash')

        # Create a new Shipment instance with all the data
        new_shipment = Shipment(
            tracking_number=tracking_number,
            status=status,
            amount=amount,
            is_paid=is_paid,
            created_at=datetime.utcnow(),
            transaction_Hash=transaction_hash
        )

        # Add the new shipment to the session and commit it to the database
        db.session.add(new_shipment)
        db.session.commit()

        flash('Shipment created successfully.', 'success')
        return redirect(url_for('shipment_bp.view_shipments'))

    return render_template('create_shipment.html')

@shipment_bp.route('/view', methods=['GET'])
def view_shipments():
    db_shipments = Shipment.query.all()
    shipments_for_rendering = []

    for db_shipment in db_shipments:
        shipments_for_rendering.append({
            'id': db_shipment.id,
            'tracking_number': db_shipment.tracking_number,
            'status': db_shipment.status,
            'amount': db_shipment.amount,
            'is_paid': 'Yes' if db_shipment.is_paid else 'No',
            'created_at': db_shipment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'transaction_Hash': db_shipment.transaction_Hash
        })

    return render_template('view_shipments.html', shipments=shipments_for_rendering)


@shipment_bp.route('/update', methods=['GET', 'POST'])
def update_shipment():
    if request.method == 'POST':
        # Extract data from the form
        tracking_number = request.form.get('trackingNumber')
        new_status = request.form.get('newStatus')

        # Fetch the shipment from the database
        shipment = Shipment.query.filter_by(tracking_number=tracking_number).first()
        if not shipment:
            flash('Shipment not found.', 'error')
            return redirect(url_for('shipment_bp.view_shipments'))

        # Update the status in the database
        shipment.status = new_status
        db.session.commit()

        flash('Shipment status updated successfully!', 'success')
        return redirect(url_for('shipment_bp.view_shipments'))
    else:
        # GET request logic
        tracking_number = request.args.get('trackingNumber', '')
        if tracking_number:
            # Fetch the shipment from the database
            shipment = Shipment.query.filter_by(tracking_number=tracking_number).first()
            if shipment:
                # Render the update template with the shipment data
                return render_template('update_shipment.html', shipment=shipment)
            else:
                flash('Shipment not found.', 'error')
                return redirect(url_for('shipment_bp.view_shipments'))
        else:
            # If no tracking number is provided, redirect to the view shipments page
            return redirect(url_for('shipment_bp.view_shipments'))