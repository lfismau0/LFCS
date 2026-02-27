"""
Management command to populate the LFIS school website with sample data.
Usage: python manage.py seed_data
"""

import io
import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils import timezone
from datetime import date, timedelta


def make_placeholder_image(width=400, height=300, color=(26, 60, 107), text="LFIS"):
    """Creates a simple solid-color PNG placeholder image using only stdlib."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', (width, height), color=color)
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, height-40, width, height], fill=(255, 193, 7))
        draw.text((width//2 - 20, height//2 - 10), text, fill=(255, 255, 255))
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()
    except ImportError:
        # Minimal valid 1x1 PNG if Pillow not available
        import struct, zlib
        def png_chunk(chunk_type, data):
            c = chunk_type + data
            return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
        r, g, b = color
        ihdr = png_chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0))
        raw = b'\x00' + bytes([r, g, b])
        idat = png_chunk(b'IDAT', zlib.compress(raw))
        iend = png_chunk(b'IEND', b'')
        return b'\x89PNG\r\n\x1a\n' + ihdr + idat + iend


def img_file(name, width=400, height=300, color=(26, 60, 107)):
    data = make_placeholder_image(width, height, color)
    return ContentFile(data, name=name)


class Command(BaseCommand):
    help = 'Seed the database with sample data for all apps'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(' Seeding LFIS sample data...'))
        self.seed_core()
        self.seed_notices()
        self.seed_school_messages()
        self.seed_facilities()
        self.seed_gallery()
        self.seed_academics()
        self.seed_staff()
        self.seed_alumni()
        self.seed_tc()
        self.seed_corner()
        self.seed_captain()
        self.seed_houses()
        self.seed_enquiries()
        self.stdout.write(self.style.SUCCESS(' Sample data seeded successfully!'))

    #  CORE 
    def seed_core(self):
        from core.models import Banner, About, ContactInfo, SocialMedia, Popup

        if not ContactInfo.objects.exists():
            ContactInfo.objects.create(
                address='Little Flower International School, Station Road, Civil Lines, Prayagraj, Uttar Pradesh - 211001',
                phone='+91-532-2400001',
                whatsapp='919532400001',
                email='info@lfisschool.edu.in',
                google_map_embed_code='<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d14399.386!2d81.8360!3d25.4358!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0!2zMjXCsDI2!5e0!3m2!1sen!2sin!4v1" width="100%" height="300" style="border:0;" allowfullscreen="" loading="lazy"></iframe>',
            )
            self.stdout.write('  OK Contact Info')

        if not SocialMedia.objects.exists():
            SocialMedia.objects.create(
                facebook_url='https://www.facebook.com/LFISschool',
                instagram_url='https://www.instagram.com/lfis_school',
                youtube_url='https://www.youtube.com/@LFISschool',
                twitter_url='https://twitter.com/lfis_school',
            )
            self.stdout.write('  OK Social Media')

        if not About.objects.exists():
            about = About(
                title='Little Flower International School',
                description='''<p>Little Flower International School (LFIS) was established in 2000 with a vision to provide quality education blended with strong moral values. Affiliated to CBSE, New Delhi, our school has consistently produced outstanding results and nurtured students to excel in academics, sports and extracurricular activities.</p>
<p>With a sprawling campus spread over 5 acres, modern infrastructure, highly qualified faculty, and a nurturing environment, LFIS stands as a beacon of educational excellence in the region.</p>
<ul>
  <li>CBSE Affiliated (Affiliation No. 2130012)</li>
  <li>Classes Nursery to XII (Science, Commerce &amp; Arts)</li>
  <li>More than 2,500 students enrolled</li>
  <li>100+ qualified and experienced faculty members</li>
</ul>''',
                vision='<p>To be a globally recognized institution that empowers students with knowledge, values and skills to become responsible citizens and leaders of tomorrow.</p>',
                mission='<p>To provide holistic education in a safe, inclusive and inspiring environment  nurturing academic excellence, creativity, character and lifelong learning.</p>',
            )
            about.image.save('about/school.png', img_file('school.png', 800, 500, (26, 60, 107)), save=True)
            self.stdout.write('  OK About')

        if not Banner.objects.exists():
            banners_data = [
                ('Excellence in Education', 'Nurturing Future Leaders Since 2000', 'Know More', '/about/', (26, 60, 107)),
                ('CBSE Affiliated School', 'Admissions Open for 2025-26', 'Apply Now', '/academics/admission/', (10, 90, 60)),
                ('State-of-the-Art Facilities', 'Smart Classrooms  Labs  Sports Complex', 'Explore', '/facilities/', (100, 30, 100)),
            ]
            for i, (title, subtitle, btn_text, btn_link, color) in enumerate(banners_data):
                b = Banner(title=title, subtitle=subtitle, button_text=btn_text, button_link=btn_link, order=i+1)
                b.image.save(f'banners/banner_{i+1}.png', img_file(f'banner_{i+1}.png', 1200, 600, color), save=True)
            self.stdout.write('  OK Banners (3)')

        if not Popup.objects.exists():
            today = timezone.now().date()
            Popup.objects.create(
                title='Admissions Open 2025-26!',
                description='Enroll your child now for the upcoming academic session. Limited seats available for all classes.',
                button_link='/academics/admission/',
                start_date=today,
                end_date=today + timedelta(days=30),
                status=True,
            )
            self.stdout.write('  OK Popup')

    #  NOTICES 
    def seed_notices(self):
        from notice_board.models import Notice
        if Notice.objects.exists():
            return
        today = timezone.now().date()
        notices = [
            ('Admission Open for 2025-26 Session', 'Admissions are now open for all classes from Nursery to Class IX and XI. Parents are requested to collect the registration forms from the school office or download from our website.', True, today, today + timedelta(days=60)),
            ('Annual Sports Day  15th March 2026', 'The Annual Sports Day will be held on 15th March 2026 at the school grounds. All students must be present in proper sports uniform by 8:00 AM.', True, today - timedelta(days=2), today + timedelta(days=20)),
            ('Parent-Teacher Meeting  5th March 2026', 'PTM for Classes VI to X will be held on 5th March 2026 (Saturday) from 9:00 AM to 1:00 PM. Parents are requested to attend.', False, today - timedelta(days=5), today + timedelta(days=10)),
            ('Half-Yearly Exam Schedule Released', 'The half-yearly examination schedule for Classes I to XII has been released. Students can collect the timetable from their respective class teachers.', False, today - timedelta(days=7), today + timedelta(days=30)),
            ('Republic Day Celebration', 'The school celebrated Republic Day with great enthusiasm. Students performed various cultural programmes. The Chief Guest was Mr. R.K. Sharma, District Magistrate.', False, today - timedelta(days=30), None),
            ('Winter Break Dates', 'The school will remain closed for Winter Break from 25th December 2025 to 5th January 2026. School reopens on 6th January 2026.', False, today - timedelta(days=45), None),
        ]
        for title, desc, imp, pub, exp in notices:
            Notice.objects.create(title=title, description=desc, is_important=imp, publish_date=pub, expiry_date=exp)
        self.stdout.write(f'  OK Notices ({len(notices)})')

    #  SCHOOL MESSAGES 
    def seed_school_messages(self):
        from school_messages.models import DirectorMessage, PrincipalMessage
        if not DirectorMessage.objects.exists():
            d = DirectorMessage(
                name='Mr. Rajesh Kumar Srivastava',
                designation='Chairman & Director',
                message='''<p>Dear Students, Parents and Well-wishers,</p>
<p>It is with great pride and immense joy that I welcome you to Little Flower International School  an institution that has been at the forefront of quality education for over two decades.</p>
<p>At LFIS, we believe that every child is unique and has unlimited potential. Our dedicated team of educators works tirelessly to bring out the best in each student  not just academically but as a complete human being.</p>
<p>We are committed to providing an environment where curiosity is celebrated, innovation is encouraged, and character is built alongside academics. Our holistic approach ensures that students graduate not only with excellent marks but with the values, skills and confidence to face the world.</p>
<p>I invite you to partner with us in this wonderful journey of shaping the future.</p>
<p><strong>Rajesh Kumar Srivastava</strong><br>Chairman &amp; Director, LFIS</p>''',
            )
            d.photo.save('messages/director/director.png', img_file('director.png', 300, 300, (26, 60, 107)), save=True)
            self.stdout.write('  OK Director Message')

        if not PrincipalMessage.objects.exists():
            p = PrincipalMessage(
                name='Mrs. Sunita Verma',
                qualification='M.Ed., Ph.D.',
                message='''<p>Dear Students and Parents,</p>
<p>Welcome to Little Flower International School! As Principal, I am honoured to lead such a vibrant community of learners, educators and parents.</p>
<p>Education is not just about acquiring knowledge  it is about developing the wisdom to use that knowledge for the greater good. At LFIS, we foster a culture of excellence, compassion, and critical thinking.</p>
<p>Our curriculum goes beyond textbooks. Through co-curricular activities, sports, arts, and community service, we ensure our students develop into well-rounded individuals ready for the challenges of the 21st century.</p>
<p>I encourage every student to dream big, work hard, and never stop learning. Together, we will achieve great things!</p>
<p><strong>Mrs. Sunita Verma</strong><br>Principal, LFIS</p>''',
            )
            p.photo.save('messages/principal/principal.png', img_file('principal.png', 300, 300, (60, 26, 107)), save=True)
            self.stdout.write('  OK Principal Message')

    #  FACILITIES 
    def seed_facilities(self):
        from facilities.models import Facility
        if Facility.objects.exists():
            return
        facilities = [
            ('Smart Classrooms', 'All classrooms are equipped with interactive smart boards, projectors, and high-speed internet connectivity for enhanced digital learning.', 'fa-chalkboard', (26, 60, 107)),
            ('Science Laboratories', 'Fully equipped Physics, Chemistry and Biology laboratories with modern instruments following CBSE guidelines for hands-on experimentation.', 'fa-flask', (10, 90, 60)),
            ('Computer Lab', 'State-of-the-art computer laboratory with 80+ latest computers, high-speed broadband, and software for coding, design and digital literacy.', 'fa-laptop', (100, 30, 100)),
            ('Library', 'A well-stocked library with over 20,000 books, magazines, journals, and digital resources to inspire a love for reading and research.', 'fa-book', (150, 80, 10)),
            ('Sports Complex', 'A sprawling sports complex with cricket ground, football field, basketball courts, badminton courts, and a fully equipped gymnasium.', 'fa-running', (20, 100, 80)),
            ('Swimming Pool', 'An Olympic-size swimming pool with trained coaches for swimming lessons from basic to advanced levels, supervised by certified lifeguards.', 'fa-swimming-pool', (0, 80, 160)),
            ('Auditorium', 'A 1,000-seat air-conditioned auditorium equipped with state-of-the-art sound and lighting systems for cultural events and seminars.', 'fa-theater-masks', (80, 20, 100)),
            ('Medical Room', 'A fully equipped medical room staffed by a qualified nurse, with first-aid facilities and emergency response protocols for student safety.', 'fa-heartbeat', (160, 30, 30)),
        ]
        for title, desc, icon, color in facilities:
            f = Facility(title=title, description=desc, icon=icon)
            f.image.save(f'facilities/{title.lower().replace(" ", "_")}.png', img_file(f'{title}.png', 400, 250, color), save=True)
        self.stdout.write(f'  OK Facilities ({len(facilities)})')

    #  GALLERY 
    def seed_gallery(self):
        from gallery.models import Album, Photo, Video
        if Album.objects.exists() and Video.objects.exists():
            return

        if not Album.objects.exists():
            albums_data = [
                ('Annual Sports Day 2025', (26, 60, 107)),
                ('Science Exhibition 2025', (10, 90, 40)),
                ('Republic Day Celebration', (180, 30, 30)),
                ('Cultural Programme 2025', (100, 30, 100)),
            ]
            for album_name, color in albums_data:
                a = Album(album_name=album_name)
                a.cover_image.save(f'gallery/covers/{album_name.replace(" ", "_")}.png',
                                   img_file(f'{album_name}.png', 600, 400, color), save=True)
                # Add 3 photos per album
                for i in range(3):
                    p = Photo(album=a, caption=f'{album_name} - Photo {i+1}')
                    p.image.save(f'gallery/photos/{album_name.replace(" ", "_")}_{i+1}.png',
                                 img_file(f'photo_{i+1}.png', 800, 600, color), save=True)
            self.stdout.write(f'  OK Albums (4) with Photos (12)')

        if not Video.objects.exists():
            videos = [
                ('Annual Day Highlights 2025', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'Highlights from our spectacular Annual Day celebration 2025'),
                ('Sports Day 2025  Opening Ceremony', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'The grand opening ceremony of Annual Sports Day 2025'),
                ('LFIS School Tour', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'Take a virtual tour of our beautiful campus and world-class facilities'),
            ]
            for title, link, desc in videos:
                Video.objects.create(title=title, youtube_link=link, description=desc)
            self.stdout.write(f'  OK Videos (3)')

    #  ACADEMICS 
    def seed_academics(self):
        from academics.models import Curriculum, FeeStructure, AdmissionProcess

        if not Curriculum.objects.exists():
            classes = ['Nursery', 'LKG', 'UKG', 'Class I', 'Class II', 'Class III',
                       'Class IV', 'Class V', 'Class VI', 'Class VII', 'Class VIII',
                       'Class IX', 'Class X', 'Class XI (Science)', 'Class XI (Commerce)', 'Class XII (Science)', 'Class XII (Commerce)']
            for cls in classes:
                Curriculum.objects.create(
                    class_name=cls,
                    description=f'<p>The curriculum for <strong>{cls}</strong> is designed as per CBSE guidelines to provide a balanced foundation in all subjects, including languages, mathematics, science, social studies, arts, and computer education.</p><p>Special emphasis is placed on conceptual understanding, application-based learning, and holistic development.</p>',
                )
            self.stdout.write(f'  OK Curriculum ({len(classes)} classes)')

        if not FeeStructure.objects.exists():
            fee_groups = [
                ('Nursery  UKG', '<table class="table table-bordered"><thead><tr><th>Fee Head</th><th>Amount ()</th></tr></thead><tbody><tr><td>Admission Fee (one-time)</td><td>5,000</td></tr><tr><td>Tuition Fee (Monthly)</td><td>2,500</td></tr><tr><td>Annual Charges</td><td>8,000</td></tr><tr><td>Transport (Optional)</td><td>1,500/month</td></tr></tbody></table>'),
                ('Class I  V', '<table class="table table-bordered"><thead><tr><th>Fee Head</th><th>Amount ()</th></tr></thead><tbody><tr><td>Admission Fee (one-time)</td><td>7,000</td></tr><tr><td>Tuition Fee (Monthly)</td><td>3,200</td></tr><tr><td>Annual Charges</td><td>10,000</td></tr><tr><td>Transport (Optional)</td><td>1,500/month</td></tr></tbody></table>'),
                ('Class VI  VIII', '<table class="table table-bordered"><thead><tr><th>Fee Head</th><th>Amount ()</th></tr></thead><tbody><tr><td>Admission Fee (one-time)</td><td>8,000</td></tr><tr><td>Tuition Fee (Monthly)</td><td>4,000</td></tr><tr><td>Annual Charges</td><td>12,000</td></tr><tr><td>Transport (Optional)</td><td>1,500/month</td></tr></tbody></table>'),
                ('Class IX  X', '<table class="table table-bordered"><thead><tr><th>Fee Head</th><th>Amount ()</th></tr></thead><tbody><tr><td>Admission Fee (one-time)</td><td>10,000</td></tr><tr><td>Tuition Fee (Monthly)</td><td>5,000</td></tr><tr><td>Annual Charges</td><td>15,000</td></tr><tr><td>Transport (Optional)</td><td>1,500/month</td></tr></tbody></table>'),
                ('Class XI  XII', '<table class="table table-bordered"><thead><tr><th>Fee Head</th><th>Amount ()</th></tr></thead><tbody><tr><td>Admission Fee (one-time)</td><td>12,000</td></tr><tr><td>Tuition Fee (Monthly)</td><td>6,500</td></tr><tr><td>Annual Charges</td><td>18,000</td></tr><tr><td>Transport (Optional)</td><td>1,500/month</td></tr></tbody></table>'),
            ]
            for cls, details in fee_groups:
                FeeStructure.objects.create(class_name=cls, fee_details=details)
            self.stdout.write(f'  OK Fee Structures (5)')

        if not AdmissionProcess.objects.exists():
            AdmissionProcess.objects.create(
                description='''<h4>Admission Process at LFIS</h4>
<p>We welcome applications for admissions to all classes subject to availability of seats. Our admission process is transparent and merit-based.</p>
<h5>Step 1: Collect Registration Form</h5>
<p>Collect the registration form from the school office or download it from our website (200 registration fee).</p>
<h5>Step 2: Submit Documents</h5>
<ul>
  <li>Birth Certificate (original + photocopy)</li>
  <li>Previous class mark sheet / Transfer Certificate</li>
  <li>Aadhaar Card of student and parents</li>
  <li>4 passport-size photographs of student</li>
  <li>Caste/Category certificate (if applicable)</li>
</ul>
<h5>Step 3: Admission Test / Interview</h5>
<p>Students seeking admission to Class I and above will appear for a short written test and/or interview. For Nursery to UKG, only an informal interaction is held.</p>
<h5>Step 4: Confirmation & Fee Payment</h5>
<p>Selected students will be notified within 3 working days. Fee must be paid within 5 days of selection to confirm the seat.</p>
<p><strong>Office Hours:</strong> Monday to Saturday, 9:00 AM to 2:00 PM<br>
<strong>Contact:</strong> +91-532-2400001 | info@lfisschool.edu.in</p>''',
            )
            self.stdout.write('  OK Admission Process')

    #  STAFF 
    def seed_staff(self):
        from staff.models import Staff
        if Staff.objects.exists():
            return
        staff_members = [
            ('Mrs. Sunita Verma', 'Principal', 'M.Ed., Ph.D.', 'management', '22 years'),
            ('Mr. Anil Kumar Singh', 'Vice Principal', 'M.Sc., B.Ed.', 'management', '18 years'),
            ('Mr. Ramesh Tiwari', 'Physics Teacher', 'M.Sc. Physics, B.Ed.', 'science', '15 years'),
            ('Mrs. Priya Sharma', 'Chemistry Teacher', 'M.Sc. Chemistry, B.Ed.', 'science', '12 years'),
            ('Mr. Deepak Pandey', 'Biology Teacher', 'M.Sc. Biology, B.Ed.', 'science', '10 years'),
            ('Mrs. Geeta Mishra', 'Mathematics Teacher', 'M.Sc. Mathematics, B.Ed.', 'maths', '16 years'),
            ('Mr. Suresh Gupta', 'Mathematics Teacher', 'M.Sc., B.Ed.', 'maths', '11 years'),
            ('Mrs. Anjali Srivastava', 'English Teacher', 'M.A. English, B.Ed.', 'english', '14 years'),
            ('Mr. Vikas Yadav', 'English Teacher', 'M.A., B.Ed.', 'english', '8 years'),
            ('Mrs. Kavita Dubey', 'Hindi Teacher', 'M.A. Hindi, B.Ed.', 'hindi', '13 years'),
            ('Mr. Ashok Shukla', 'Social Studies Teacher', 'M.A. History, B.Ed.', 'social', '17 years'),
            ('Mrs. Pooja Tripathi', 'Computer Science Teacher', 'MCA, B.Ed.', 'computer', '9 years'),
            ('Mr. Rohit Keshari', 'Sports Coach', 'B.P.Ed., M.P.Ed.', 'sports', '7 years'),
            ('Mrs. Meena Singh', 'Art & Craft Teacher', 'B.F.A., M.F.A.', 'arts', '11 years'),
            ('Mr. Mohit Aggarwal', 'Office Administrator', 'B.Com, MBA', 'administration', '6 years'),
        ]
        colors = [(26, 60, 107), (60, 26, 107), (107, 60, 26), (10, 90, 60), (90, 10, 60)]
        for i, (name, desig, qual, dept, exp) in enumerate(staff_members):
            s = Staff(name=name, designation=desig, qualification=qual, department=dept, experience=exp)
            color = colors[i % len(colors)]
            s.photo.save(f'staff/{name.replace(" ", "_").replace(".", "")}.png',
                         img_file(f'{name}.png', 300, 300, color), save=True)
        self.stdout.write(f'  OK Staff ({len(staff_members)})')

    #  ALUMNI 
    def seed_alumni(self):
        from alumni.models import Alumni
        if Alumni.objects.exists():
            return
        alumni_data = [
            ('Rahul Srivastava', '2015', 'IAS Officer, UP Cadre', 'Selected for IAS in UPSC 2019, currently posted as District Magistrate'),
            ('Priya Gupta', '2015', 'Software Engineer at Google', 'Currently working at Google Bengaluru after completing B.Tech from IIT Delhi'),
            ('Amit Kumar', '2016', 'Doctor (MBBS, AIIMS)', 'Completed MBBS from AIIMS Delhi, currently pursuing MD Cardiology'),
            ('Neha Verma', '2016', 'IPS Officer', 'Selected for IPS in UPSC 2020, currently posted in Lucknow'),
            ('Sandeep Pandey', '2017', 'CA & Financial Analyst', 'Chartered Accountant, working with Deloitte India in Mumbai'),
            ('Ankita Tiwari', '2017', 'Scientist, ISRO', 'Working as scientist at ISRO Bengaluru on satellite communication projects'),
            ('Ravi Shankar', '2018', 'Army Officer (Captain)', 'Commissioned as Captain in Indian Army, 5th Gorkha Rifles'),
            ('Divya Singh', '2018', 'Fashion Designer', 'Running own fashion brand "Divinity by Divya" in Delhi'),
            ('Mohit Keshari', '2019', 'Software Developer at TCS', 'Working as full-stack developer after completing B.Tech from NIT Allahabad'),
            ('Shreya Mishra', '2019', 'National Badminton Player', 'Represented UP State in National Badminton Championship 2023'),
            ('Vivek Yadav', '2020', 'Civil Engineer', 'Working with L&T Construction after completing B.Tech from VIT Vellore'),
            ('Ritika Dubey', '2020', 'Journalist, Times of India', 'Working as correspondent covering education and social issues'),
        ]
        colors = [(26, 60, 107), (107, 60, 26), (60, 107, 26), (60, 26, 107)]
        for i, (name, batch, profession, achievement) in enumerate(alumni_data):
            a = Alumni(name=name, batch=batch, profession=profession, achievement=achievement)
            a.photo.save(f'alumni/{name.replace(" ", "_").replace(".", "")}.png',
                         img_file(f'{name}.png', 200, 200, colors[i % len(colors)]), save=True)
        self.stdout.write(f'  OK Alumni ({len(alumni_data)})')

    #  TRANSFER CERTIFICATES 
    def seed_tc(self):
        from tc.models import TC
        if TC.objects.exists():
            return
        tc_data = [
            ('Sanjay Kumar Sharma', 'Class X', 'Rajesh Kumar Sharma', 'LFIS/2020/001', 'TC/2020/001', date(2020, 3, 25)),
            ('Pooja Devi', 'Class IX', 'Ramesh Devi', 'LFIS/2021/002', 'TC/2021/002', date(2021, 4, 10)),
            ('Aman Verma', 'Class VIII', 'Suresh Verma', 'LFIS/2021/003', 'TC/2021/003', date(2021, 5, 5)),
            ('Nikita Singh', 'Class XII', 'Harendra Singh', 'LFIS/2022/004', 'TC/2022/004', date(2022, 3, 20)),
            ('Rohit Gupta', 'Class X', 'Vinod Gupta', 'LFIS/2022/005', 'TC/2022/005', date(2022, 4, 15)),
        ]
        for student, cls, father, adm, tc, issue in tc_data:
            TC.objects.create(student_name=student, student_class=cls, father_name=father,
                              admission_no=adm, tc_number=tc, issue_date=issue)
        self.stdout.write(f'  OK Transfer Certificates ({len(tc_data)})')

    #  CORNER 
    def seed_corner(self):
        from corner.models import Corner
        if Corner.objects.exists():
            return
        items = [
            ('student', 'Attendance Policy', 'Students must maintain a minimum 75% attendance to be eligible for examinations. Regular attendance is essential for academic progress.'),
            ('student', 'Examination Guidelines', 'Important guidelines for all examinations: Arrive 15 minutes before exam time, carry your admit card, and follow the hall rules strictly.'),
            ('student', 'Scholarship Opportunities', 'LFIS offers merit scholarships to top 3 students of each class. Apply before 30th April every year with previous year report card.'),
            ('student', 'Student Council Elections', 'Student Council elections for 2025-26 will be held on 20th March. Students of Classes IX-XII are eligible to vote and contest.'),
            ('teacher', 'Staff Leave Policy', 'Teaching staff may apply for causal leave (12 days/year) and medical leave (10 days/year) through the Staff Management Portal.'),
            ('teacher', 'Lesson Plan Submission', 'All teachers must submit monthly lesson plans by the 25th of the preceding month to the Vice Principal for review and approval.'),
            ('teacher', 'Professional Development Workshop', 'A 2-day in-house training workshop on "Innovative Teaching Methodologies" will be held on 8-9 March 2026. Attendance is compulsory.'),
            ('parent', 'Parent Portal Access', 'Parents can access their child progress, attendance, and fee payment history through the LFIS Parent Portal at parent.lfisschool.edu.in'),
            ('parent', 'Parent-Teacher Meeting Schedule', 'PTMs are held every quarter. The next PTM is scheduled for 5th March 2026 (Saturday). Please ensure your attendance.'),
            ('parent', 'Fee Payment Information', 'Fees can be paid online through the parent portal or at the school office. Late fee will be charged after the 10th of each month.'),
        ]
        for category, title, desc in items:
            Corner.objects.create(category=category, title=title, description=desc)
        self.stdout.write(f'  OK Corner Items ({len(items)})')

    #  CAPTAIN 
    def seed_captain(self):
        from captain.models import SchoolCaptain
        if SchoolCaptain.objects.exists():
            return
        captains = [
            ('Arjun Pratap Singh', 'Class XII-A', '2025', 'It is a great honour to serve as School Captain. I promise to uphold the values of LFIS and represent every student with pride and dedication.'),
            ('Ananya Srivastava', 'Class XII-B', '2024', 'Being School Captain has been a life-changing experience. I am grateful to my teachers, parents, and classmates for their support.'),
        ]
        colors = [(26, 60, 107), (60, 26, 107)]
        for i, (name, cls, year, msg) in enumerate(captains):
            c = SchoolCaptain(name=name, student_class=cls, year=year, message=msg)
            c.photo.save(f'captain/{name.replace(" ", "_")}.png',
                         img_file(f'{name}.png', 300, 300, colors[i % len(colors)]), save=True)
        self.stdout.write(f'  OK School Captains ({len(captains)})')

    #  HOUSES 
    def seed_houses(self):
        from house.models import House, HouseLeader
        if House.objects.exists():
            return
        houses = [
            ('Nehru House', 'Blue', (26, 60, 160)),
            ('Gandhi House', 'Green', (26, 140, 60)),
            ('Shivaji House', 'Red', (160, 30, 30)),
            ('Tagore House', 'Yellow', (180, 140, 10)),
        ]
        for house_name, color_name, rgb in houses:
            h = House(house_name=house_name, color=color_name)
            h.save()
            HouseLeader.objects.create(
                house=h,
                head_boy=f'{house_name.split()[0]} Head Boy',
                head_girl=f'{house_name.split()[0]} Head Girl',
                vice_head_boy=f'{house_name.split()[0]} Vice Head Boy',
                vice_head_girl=f'{house_name.split()[0]} Vice Head Girl',
                year='2025-26',
            )
        self.stdout.write(f'  OK Houses (4) with House Leaders')

    #  ENQUIRIES 
    def seed_enquiries(self):
        from enquiry.models import Enquiry
        if Enquiry.objects.exists():
            return
        enquiries = [
            ('Rajesh Sharma', '+91-9876543210', 'rajesh@email.com', 'I would like to know about admission procedure for my child in Class I for session 2025-26.', 'Class I', 'new'),
            ('Priya Verma', '+91-8765432109', 'priya.verma@gmail.com', 'Kindly share the fee structure and facilities available at LFIS for senior classes.', 'Class XI', 'replied'),
            ('Suresh Kumar', '+91-7654321098', '', 'I want to enquire about the transport facility available from Civil Lines area.', '', 'new'),
        ]
        for name, phone, email, msg, cls, status in enquiries:
            Enquiry.objects.create(name=name, phone=phone, email=email, message=msg, class_interested=cls, status=status)
        self.stdout.write(f'  OK Sample Enquiries ({len(enquiries)})')

