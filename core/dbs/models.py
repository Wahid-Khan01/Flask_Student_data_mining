from core import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    is_fresher = db.Column(db.Boolean, nullable=False)
    allow_updates = db.Column(db.Boolean, default=False)

    # Define one-to-many relationship with PDFModel
    pdf_files = db.relationship('PDFModel', backref='user', lazy=True)

    # Define one-to-one relationship with ResumeHeadline
    resume_headline = db.relationship('ResumeHeadline', uselist=False, backref='user', lazy=True)
    educations = db.relationship('Education', backref='user', lazy=True)
    basicdetailsfresher = db.relationship('BasicDetailsFresher', backref='user', lazy=True)

class PDFModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"PDFModel(id={self.id})"

class ResumeHeadline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String, nullable=False)

    # Define foreign key to User model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Resume Headline of {self.id}"
    
class UserSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skills = db.Column(db.String(500), nullable=False)  # Store comma-separated skills

    def __repr__(self):
        return f"UserSkill(id={self.id}, user_id={self.user_id}, skills={self.skills})"

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    education = db.Column(db.String, nullable=False)
    university = db.Column(db.String, nullable=False)
    course = db.Column(db.String, nullable=False)
    specialization = db.Column(db.String, nullable=False)
    course_type = db.Column(db.String, nullable=False)
    course_duration_from_year = db.Column(db.Integer, nullable=False)
    course_duration_to_year = db.Column(db.Integer, nullable=False)
    marks = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Education(id={self.id}, education={self.education}, university={self.university}, course={self.course})"

    def serialize(self):
        return {
            'id': self.id,
            'education': self.education,
            'university': self.university,
            'course': self.course,
            'specialization': self.specialization,
            'course_type': self.course_type,
            'course_duration_from_year': self.course_duration_from_year,
            'course_duration_to_year': self.course_duration_to_year,
            'marks': self.marks
        }




class BasicDetailsFresher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    is_fresher = db.Column(db.Boolean())
    country_india = db.Column(db.Boolean())
    country_outside_india = db.Column(db.Boolean())
    location = db.Column(db.String(100))
    country_name = db.Column(db.String(100))

    phone = db.Column(db.String(20))  
    email = db.Column(db.String(100))
    availability = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Fresher {self.name}>'