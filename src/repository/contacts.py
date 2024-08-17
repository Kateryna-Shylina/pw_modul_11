from typing import List

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel

from datetime import datetime
from datetime import datetime, timedelta

from sqlalchemy import func


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(first_name=body.first_name, last_name=body.last_name, email=body.email, phone=body.phone, birthday_date = body.birthday_date)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday_date = body.birthday_date  
        db.commit()
    return contact


async def update_birthday(contact_id: int, birthday_date: datetime, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.birthday_date = birthday_date
        db.commit()
        db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session)  -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(query: str, db: Session) -> List[Contact]:
    return db.query(Contact).filter(
        (Contact.first_name.ilike(f"%{query}%")) |
        (Contact.last_name.ilike(f"%{query}%")) |
        (Contact.email.ilike(f"%{query}%"))
    ).all()


async def get_upcoming_birthdays(db: Session) -> List[Contact]:
    today = datetime.now().date()
    days_ahead = [(today + timedelta(days=i)).strftime('%m-%d') for i in range(8)]

    contacts = db.query(Contact).filter(
        func.to_char(Contact.birthday_date, 'MM-DD').in_(days_ahead)
    ).all()
    return contacts