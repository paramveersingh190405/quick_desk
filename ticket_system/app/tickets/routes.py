from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.tickets import bp
from app.models import Ticket
from app.forms import TicketForm
from datetime import datetime

@bp.route('/dashboard')
@login_required
def dashboard():
    page = request.args.get('page', 1, type=int)
    tickets = Ticket.query.filter_by(user_id=current_user.id)\
        .order_by(Ticket.date_posted.desc())\
        .paginate(page=page, per_page=5)
    
    stats = {
        'open': Ticket.query.filter_by(user_id=current_user.id, status='Open').count(),
        'in_progress': Ticket.query.filter_by(user_id=current_user.id, status='In Progress').count(),
        'closed': Ticket.query.filter_by(user_id=current_user.id, status='Closed').count()
    }
    
    return render_template('tickets/dashboard.html', tickets=tickets, stats=stats)

@bp.route('/ticket/new', methods=['GET', 'POST'])
@login_required
def create():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            title=form.title.data,
            content=form.content.data,
            status=form.status.data,
            author=current_user
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Your ticket has been created!', 'success')
        return redirect(url_for('tickets.dashboard'))
    return render_template('tickets/create.html', title='New Ticket', form=form)

@bp.route('/ticket/<int:ticket_id>')
@login_required
def ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.author != current_user:
        flash('You are not authorized to view this ticket', 'danger')
        return redirect(url_for('tickets.dashboard'))
    return render_template('tickets/detail.html', ticket=ticket)

@bp.route('/ticket/<int:ticket_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.author != current_user:
        flash('You are not authorized to edit this ticket', 'danger')
        return redirect(url_for('tickets.dashboard'))
    
    form = TicketForm()
    if form.validate_on_submit():
        ticket.title = form.title.data
        ticket.content = form.content.data
        ticket.status = form.status.data
        db.session.commit()
        flash('Your ticket has been updated!', 'success')
        return redirect(url_for('tickets.ticket', ticket_id=ticket.id))
    elif request.method == 'GET':
        form.title.data = ticket.title
        form.content.data = ticket.content
        form.status.data = ticket.status
    return render_template('tickets/create.html', title='Edit Ticket', form=form)

@bp.route('/ticket/<int:ticket_id>/delete', methods=['POST'])
@login_required
def delete(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.author != current_user:
        flash('You are not authorized to delete this ticket', 'danger')
        return redirect(url_for('tickets.dashboard'))
    db.session.delete(ticket)
    db.session.commit()
    flash('Your ticket has been deleted!', 'success')
    return redirect(url_for('tickets.dashboard'))