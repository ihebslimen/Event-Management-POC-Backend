
from utils.db import db

class Event(db.Model):
    __tablename__ = 'event'


    # 🔑 Primary Keys & Identifiers
    id = db.Column(db.Integer, primary_key=True)
    #uuid = db.Column(db.String(36), unique=True, nullable=False)  # useful for public URLs
    #slug = db.Column(db.String(255), unique=True, nullable=False)  # SEO-friendly name

    # 📌 Basic Info
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(255))
    description = db.Column(db.Text)

    # 📍 Location & Venue
    location_name = db.Column(db.String(255))   # e.g., "Conference Hall A"
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    is_online = db.Column(db.Boolean, default=False)
    online_link = db.Column(db.String(255))  # Zoom/Meet/Custom link

    # 🗓 Date & Time
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    timezone = db.Column(db.String(50), default="UTC")
    recurrence_rule = db.Column(db.String(255))  # iCal-style recurrence rule frequency day month year 

    # 🎟 Ticketing / Registration
    registration_required = db.Column(db.Boolean, default=False)
    max_attendees = db.Column(db.Integer)  # total seats
    tickets_available = db.Column(db.Integer)  # dynamically updated
    ticket_price = db.Column(db.Float)  # single price, or
    ticket_currency = db.Column(db.String(10), default="USD")
    ticket_types = db.Column(db.JSON)  # {"VIP": 100, "General": 50}

    # 👥 Organizers / Hosts
    organizer = db.Column(db.String(255))
    organizer_contact = db.Column(db.String(255))  # email/phone
    co_hosts = db.Column(db.JSON)  # multiple collaborators

    # 📢 Marketing & Metadata
    banner_image = db.Column(db.String(255))
    thumbnail_image = db.Column(db.String(255))
    tags = db.Column(db.JSON)
    category = db.Column(db.String(100))  # Conference, Webinar, Concert
    website_url = db.Column(db.String(255))
    social_links = db.Column(db.JSON)  # {"facebook": "...", "instagram": "..."}

    # 📊 Engagement & Interaction
    attendees_count = db.Column(db.Integer, default=0)
    views_count = db.Column(db.Integer, default=0)
    likes_count = db.Column(db.Integer, default=0)
    shares_count = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)

    # ✅ Status & Access Control
    is_public = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)   #normal or important
    status = db.Column(db.String(50), default="draft")  # draft, published, cancelled
    access_code = db.Column(db.String(50))  # private events

    # 🕒 Audit Fields
    #created_at = db.Column(db.DateTime, default=datetime.utcnow)
    #updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'subtitle': self.subtitle,
            'description': self.description,
            'location_name': self.location_name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'is_online': self.is_online,
            'online_link': self.online_link,
            'start_datetime': self.start_datetime.isoformat() if self.start_datetime else None,
            'end_datetime': self.end_datetime.isoformat() if self.end_datetime else None,
            'timezone': self.timezone,
            'recurrence_rule': self.recurrence_rule,
            'registration_required': self.registration_required,
            'max_attendees': self.max_attendees,
            'tickets_available': self.tickets_available,
            'ticket_price': self.ticket_price,
            'ticket_currency': self.ticket_currency,
            'ticket_types': self.ticket_types,
            'organizer': self.organizer,
            'organizer_contact': self.organizer_contact,
            'co_hosts': self.co_hosts,
            'banner_image': self.banner_image,
            'thumbnail_image': self.thumbnail_image,
            'tags': self.tags,
            'category': self.category,
            'website_url': self.website_url,
            'social_links': self.social_links,
            'attendees_count': self.attendees_count,
            'views_count': self.views_count,
            'likes_count': self.likes_count,
            'shares_count': self.shares_count,
            'rating': self.rating,
            'is_public': self.is_public,
            'is_featured': self.is_featured,
            'status': self.status,
            'access_code': self.access_code,
        }

