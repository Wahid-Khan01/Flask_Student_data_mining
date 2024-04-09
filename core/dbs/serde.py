from marshmallow import Schema, fields, validate
from datetime import datetime

class users_schema(Schema):
    id = fields.Int(dump_only=True)
    full_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    mobile_number = fields.Int(required=True)
    is_fresher = fields.Boolean(required=True)
    allow_updates = fields.Boolean()
    pdf_files = fields.Nested('PDFModelSchema', many=True)  # Foreign key for PDFModel
    resume_headline = fields.Nested('ResumeHeadlineSchema')  


class PDFModelSchema(Schema):
    id = fields.Int(dump_only=True)
    data = fields.Str(required=True)
    user_id = fields.Int()

class ResumeHeadlineSchema(Schema):
    id = fields.Int(dump_only=True)
    headline = fields.Str(required=True)

class UserSkillSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    skill = fields.Str(required=True, validate=validate.Length(max=100))



COURSE_TYPE_CHOICES = ["full time", "part time", "Correspondence/distance learning"]
EDUCATION_CHOICES = ["Doctorate/PhD","Masters/Post-Graduation","Graduation/Diploma","12th",'10th',"Below 10th"]
COURSE_DURATION_CHOICES = ["2 years", "3 years", "4 years", "5 years", "Present"]
YEAR_CHOICES = [(year, year) for year in range(datetime.now().year - 80, datetime.now().year + 1)]

class education_schema(Schema):
    id = fields.Int(dump_only=True)
    education = fields.Str(required=True, validate=validate.OneOf(EDUCATION_CHOICES))
    university = fields.Str(required=True)
    course = fields.Str(required=True)
    specialization = fields.Str(required=True)
    course_type = fields.Str(required=True, validate=validate.OneOf(COURSE_TYPE_CHOICES))
    course_duration_from_year = fields.Int(required=True, validate=validate.OneOf([year[0] for year in YEAR_CHOICES]))
    course_duration_to_year = fields.Int(required=True, validate=validate.OneOf([year[0] for year in YEAR_CHOICES]))
    marks = fields.Str(required=True),
    user_id = fields.Int(required=True)


AVAILABILITY_CHOICES = ["15 Days or less", "1 Month", "2 Months","3 Months","More than 3 Months"]
class BasicDetailsFresher_schema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    is_fresher =  fields.Boolean(required=True)  
    country_india = fields.Boolean(required=True)
    country_outside_india = fields.Boolean(required=True) 
    location=fields.Boolean(required=True)   
    country_name=fields.Str(required=True)
    phone =fields.Int(required=True)
    email = fields.Str(required=True)
    availability = fields.Str(required=True, validate=validate.OneOf(AVAILABILITY_CHOICES))
    user_id = fields.Int(required=True)

