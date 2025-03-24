@app.route('/claim/<int:item_id>', methods=['POST'])
@login_required
def claim_item(item_id):
    print(f"Claim request received for item_id: {item_id}")  # Debugging line

    item = Item.query.get_or_404(item_id)
    existing_claim = ClaimedItem.query.filter_by(item_id=item_id, student_num=current_user.student_num).first()

    if existing_claim:
        flash("You have already claimed this item.", "warning")
        return redirect(url_for('home'))

    new_claim = ClaimedItem(
        student_num=current_user.student_num,
        item_id=item_id,
        approval=False  # Initially not approved
    )

    db.session.add(new_claim)
    db.session.commit()
    flash("You have successfully claimed the item.", "success")

    print(f"Item {item_id} claimed by {current_user.student_num}")  # Debugging line
    return redirect(url_for('home'))