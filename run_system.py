#!/usr/bin/env python3
"""
نظام إرسال السيرة الذاتية الآلي
CV Sending Automation System
"""

import os
import sys
import json
import time
import logging
import schedule
import smtplib
import requests
from datetime import datetime
from typing import Dict, List, Optional
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import pandas as pd
from bs4 import BeautifulSoup
import re

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cv_automation.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CVAutomationSystem:
    """نظام إرسال السيرة الذاتية الآلي"""
    
    def __init__(self, config_file: str = "user_config.json"):
        self.config_file = config_file
        self.user_config = {}
        self.csv_file = "companies_emails.csv"
        self.sent_emails_file = "sent_emails.csv"
        
        # تحميل إعدادات المستخدم
        self.load_user_config()
        
        # إعداد ملف CSV
        self.setup_csv_files()
        
    def load_user_config(self):
        """تحميل إعدادات المستخدم"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.user_config = json.load(f)
                logger.info("تم تحميل إعدادات المستخدم بنجاح")
            else:
                logger.error(f"ملف الإعدادات غير موجود: {self.config_file}")
                print("❌ ملف الإعدادات غير موجود!")
                print("🔧 يرجى تشغيل: python3 user_setup.py")
                sys.exit(1)
        except Exception as e:
            logger.error(f"خطأ في تحميل الإعدادات: {e}")
            sys.exit(1)
    
    def setup_csv_files(self):
        """إعداد ملفات CSV"""
        # ملف الشركات والإيميلات
        if not os.path.exists(self.csv_file):
            df = pd.DataFrame(columns=pd.Index(['company_name', 'email', 'source_url', 'city', 'country']))
            df.to_csv(self.csv_file, index=False, encoding='utf-8')
            logger.info(f"تم إنشاء ملف: {self.csv_file}")
        
        # ملف الإيميلات المرسلة
        if not os.path.exists(self.sent_emails_file):
            df = pd.DataFrame(columns=pd.Index(['email', 'company_name', 'sent_date', 'status']))
            df.to_csv(self.sent_emails_file, index=False, encoding='utf-8')
            logger.info(f"تم إنشاء ملف: {self.sent_emails_file}")
    
    def validate_email(self, email: str) -> bool:
        """التحقق من صحة الإيميل"""
        if not email or '@' not in email:
            return False
        
        # قائمة الإيميلات المرفوضة
        rejected_patterns = [
            'noreply', 'no-reply', 'donotreply', 'do-not-reply',
            'test', 'example', 'localhost', 'admin@',
            '.comp', '.comcall', '.co.uk.', '.sa.', '.ae.'
        ]
        
        email_lower = email.lower()
        for pattern in rejected_patterns:
            if pattern in email_lower:
                return False
        
        # التحقق من صيغة الإيميل
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None
    
    def search_companies(self, city: str, job_title: str) -> List[Dict]:
        """البحث عن الشركات"""
        companies = []
        
        # قائمة مصطلحات البحث
        search_terms = [
            f"software companies in {city}",
            f"IT companies {city}",
            f"web development companies {city}",
            f"mobile app development {city}",
            f"software development {city}",
            f"tech companies {city}",
            f"{job_title} jobs {city}"
        ]
        
        for term in search_terms:
            try:
                # محاكاة البحث (يمكن تطويرها لاستخدام APIs حقيقية)
                logger.info(f"البحث عن: {term}")
                
                # هنا يمكن إضافة APIs حقيقية للبحث
                # مؤقتاً سنستخدم قائمة افتراضية
                mock_companies = self.get_mock_companies(city)
                companies.extend(mock_companies)
                
                time.sleep(2)  # تجنب الحظر
                
            except Exception as e:
                logger.error(f"خطأ في البحث عن {term}: {e}")
        
        return companies
    
    def get_mock_companies(self, city: str) -> List[Dict]:
        """الحصول على قائمة شركات افتراضية (للاختبار)"""
        mock_companies = [
            {"name": f"Tech Solutions {city}", "email": f"hr@techsolutions{city.lower().replace(' ', '')}.com", "url": f"https://techsolutions{city.lower().replace(' ', '')}.com"},
            {"name": f"Digital Innovation {city}", "email": f"careers@digitalinnovation{city.lower().replace(' ', '')}.com", "url": f"https://digitalinnovation{city.lower().replace(' ', '')}.com"},
            {"name": f"Software House {city}", "email": f"info@softwarehouse{city.lower().replace(' ', '')}.com", "url": f"https://softwarehouse{city.lower().replace(' ', '')}.com"},
            {"name": f"Web Development Co {city}", "email": f"contact@webdev{city.lower().replace(' ', '')}.com", "url": f"https://webdev{city.lower().replace(' ', '')}.com"},
            {"name": f"Mobile Apps {city}", "email": f"jobs@mobileapps{city.lower().replace(' ', '')}.com", "url": f"https://mobileapps{city.lower().replace(' ', '')}.com"}
        ]
        return mock_companies
    
    def extract_emails_from_website(self, url: str) -> List[str]:
        """استخراج الإيميلات من موقع الشركة"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # البحث عن الإيميلات
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, response.text)
            
            # تنظيف وتصفية الإيميلات
            valid_emails = []
            for email in emails:
                if self.validate_email(email):
                    valid_emails.append(email.lower())
            
            return list(set(valid_emails))  # إزالة المكرر
            
        except Exception as e:
            logger.error(f"خطأ في استخراج الإيميلات من {url}: {e}")
            return []
    
    def save_companies_to_csv(self, companies: List[Dict], city: str):
        """حفظ الشركات في ملف CSV"""
        try:
            df = pd.read_csv(self.csv_file, encoding='utf-8')
            
            new_data = []
            for company in companies:
                # التحقق من عدم وجود الشركة مسبقاً
                if not df[df['email'] == company['email']].empty:
                    continue
                
                new_data.append({
                    'company_name': company['name'],
                    'email': company['email'],
                    'source_url': company['url'],
                    'city': city,
                    'country': self.get_country_from_city(city)
                })
            
            if new_data:
                new_df = pd.DataFrame(new_data)
                df = pd.concat([df, new_df], ignore_index=True)
                df.to_csv(self.csv_file, index=False, encoding='utf-8')
                logger.info(f"تم حفظ {len(new_data)} شركة جديدة")
            
        except Exception as e:
            logger.error(f"خطأ في حفظ الشركات: {e}")
    
    def get_country_from_city(self, city: str) -> str:
        """تحديد الدولة من المدينة"""
        saudi_cities = ["الرياض", "جدة", "الدمام", "مكة المكرمة", "المدينة المنورة", "الطائف", "تبوك", "الأحساء", "بريدة", "خميس مشيط"]
        uae_cities = ["دبي", "أبوظبي", "الشارقة", "عجمان", "الفجيرة", "رأس الخيمة", "أم القيوين"]
        kuwait_cities = ["الكويت", "الأحمدي", "الفروانية", "الجهراء", "حولي", "مبارك الكبير"]
        jordan_cities = ["عمان", "الزرقاء", "إربد", "الرصيفة", "الطفيلة", "الكرك", "معان", "العقبة"]
        oman_cities = ["مسقط", "صلالة", "نزوى", "صور", "صحار", "الرستاق", "البريمي"]
        
        if city in saudi_cities:
            return "السعودية"
        elif city in uae_cities:
            return "الإمارات"
        elif city in kuwait_cities:
            return "الكويت"
        elif city in jordan_cities:
            return "الأردن"
        elif city in oman_cities:
            return "عمان"
        else:
            return "غير محدد"
    
    def create_email_template(self, company_name: str) -> str:
        """إنشاء قالب الإيميل"""
        name = self.user_config.get('name', 'المتقدم')
        phone = self.user_config.get('phone', '')
        email = self.user_config.get('email', '')
        job_title = self.user_config.get('job_title', 'Software Developer')
        
        template = f"""Subject: {job_title} Application - {company_name}

Dear {company_name} Team,

I hope this email finds you well. I am writing to express my strong interest in {job_title} opportunities at {company_name}.

As an experienced professional with a proven track record in software development and project management, I am excited about the possibility of contributing to your organization's growth and success. I have attached my CV for your review, which outlines my technical expertise and key achievements.

My background includes:
• Leading development teams and managing software projects
• Full-stack development with modern technologies
• Implementing best practices and agile methodologies
• Delivering high-quality solutions on time and within budget
• Strong communication and problem-solving skills

I would be grateful for the opportunity to discuss how my skills and experience can benefit {company_name}. I am available for an interview at your convenience and am open to relocation if required.

Thank you for considering my application. I look forward to hearing from you.

Best regards,
{name}
{phone}
{email}

---
This email was sent as part of my job application process. If you have received this email in error, please disregard it.
"""
        return template
    
    def send_email(self, recipient_email: str, company_name: str) -> bool:
        """إرسال الإيميل"""
        try:
            # إعداد الإيميل
            msg = MIMEMultipart()
            msg['From'] = self.user_config['email']
            msg['To'] = recipient_email
            msg['Subject'] = f"{self.user_config['job_title']} Application - {company_name}"
            
            # إضافة محتوى الإيميل
            email_body = self.create_email_template(company_name)
            msg.attach(MIMEText(email_body, 'plain'))
            
            # إرفاق السيرة الذاتية
            cv_path = self.user_config.get('cv_file', 'cv.pdf')
            if os.path.exists(cv_path):
                with open(cv_path, 'rb') as file:
                    attach = MIMEApplication(file.read(), _subtype='pdf')
                    attach.add_header('Content-Disposition', 'attachment', filename='cv.pdf')
                    msg.attach(attach)
            else:
                logger.warning(f"ملف السيرة الذاتية غير موجود: {cv_path}")
                return False
            
            # إرسال الإيميل
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.user_config['email'], self.user_config['app_password'])
                server.send_message(msg)
            
            logger.info(f"تم إرسال الإيميل بنجاح إلى {recipient_email} ({company_name})")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في إرسال الإيميل إلى {recipient_email}: {e}")
            return False
    
    def mark_email_as_sent(self, email: str, company_name: str, status: str = "sent"):
        """تسجيل الإيميل كمرسل"""
        try:
            df = pd.read_csv(self.sent_emails_file, encoding='utf-8')
            
            new_record = {
                'email': email,
                'company_name': company_name,
                'sent_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': status
            }
            
            df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
            df.to_csv(self.sent_emails_file, index=False, encoding='utf-8')
            
        except Exception as e:
            logger.error(f"خطأ في تسجيل الإيميل المرسل: {e}")
    
    def get_unsent_emails(self, limit: int = 30) -> List[Dict]:
        """الحصول على الإيميلات غير المرسلة"""
        try:
            companies_df = pd.read_csv(self.csv_file, encoding='utf-8')
            sent_df = pd.read_csv(self.sent_emails_file, encoding='utf-8')
            
            # استبعاد الإيميلات المرسلة
            sent_emails = sent_df['email'].tolist()
            unsent_companies = companies_df[~companies_df['email'].isin(sent_emails)]
            
            return unsent_companies.head(limit).to_dict(orient='records')
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على الإيميلات غير المرسلة: {e}")
            return []
    
    def scrape_companies_job(self):
        """مهمة البحث عن الشركات"""
        logger.info("بدء مهمة البحث عن الشركات")
        
        cities = self.user_config.get('target_cities', [])
        job_title = self.user_config.get('job_title', 'Software Developer')
        
        total_companies = 0
        
        for city in cities:
            logger.info(f"البحث في مدينة: {city}")
            
            companies = self.search_companies(city, job_title)
            
            if companies:
                self.save_companies_to_csv(companies, city)
                total_companies += len(companies)
                logger.info(f"تم العثور على {len(companies)} شركة في {city}")
            
            time.sleep(3)  # تجنب الحظر
        
        logger.info(f"انتهت مهمة البحث. إجمالي الشركات: {total_companies}")
    
    def send_emails_job(self):
        """مهمة إرسال الإيميلات"""
        logger.info("بدء مهمة إرسال الإيميلات")
        
        unsent_emails = self.get_unsent_emails(30)
        
        if not unsent_emails:
            logger.info("لا توجد إيميلات غير مرسلة")
            return
        
        sent_count = 0
        
        for company in unsent_emails:
            email = company['email']
            company_name = company['company_name']
            
            logger.info(f"إرسال إيميل إلى {email} ({company_name})")
            
            if self.send_email(email, company_name):
                self.mark_email_as_sent(email, company_name, "sent")
                sent_count += 1
            else:
                self.mark_email_as_sent(email, company_name, "failed")
            
            time.sleep(10)  # تأخير بين الإرسالات
        
        logger.info(f"انتهت مهمة الإرسال. تم إرسال {sent_count} إيميل")
    
    def setup_scheduler(self):
        """إعداد المجدول"""
        schedule_type = self.user_config.get('schedule_type', 'immediate')
        
        if schedule_type == 'immediate':
            logger.info("تشغيل فوري")
            self.scrape_companies_job()
            self.send_emails_job()
            
        elif schedule_type == 'daily':
            schedule_time = self.user_config.get('schedule_time', '14:00')
            logger.info(f"تشغيل يومي في الساعة {schedule_time}")
            
            # جدولة البحث عن الشركات
            schedule.every().day.at(schedule_time).do(self.scrape_companies_job)
            
            # جدولة إرسال الإيميلات (بعد ساعة من البحث)
            hour, minute = map(int, schedule_time.split(':'))
            send_hour = (hour + 1) % 24
            send_time = f"{send_hour:02d}:{minute:02d}"
            schedule.every().day.at(send_time).do(self.send_emails_job)
            
        elif schedule_type == 'weekly':
            schedule_day = self.user_config.get('schedule_day', 0)  # 0 = Sunday
            schedule_time = self.user_config.get('schedule_time', '14:00')
            
            days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
            day_name = days[schedule_day]
            
            logger.info(f"تشغيل أسبوعي كل {day_name} في الساعة {schedule_time}")
            
            getattr(schedule.every(), day_name).at(schedule_time).do(self.scrape_companies_job)
            
            # إرسال الإيميلات بعد ساعة
            hour, minute = map(int, schedule_time.split(':'))
            send_hour = (hour + 1) % 24
            send_time = f"{send_hour:02d}:{minute:02d}"
            getattr(schedule.every(), day_name).at(send_time).do(self.send_emails_job)
            
        elif schedule_type == 'monthly':
            logger.info("التشغيل الشهري يتطلب إعداد خاص")
            # يمكن تطوير هذا لاحقاً
    
    def run(self):
        """تشغيل النظام"""
        logger.info("بدء تشغيل نظام إرسال السيرة الذاتية")
        
        # التحقق من وجود ملف السيرة الذاتية
        cv_path = self.user_config.get('cv_file', 'cv.pdf')
        if not os.path.exists(cv_path):
            logger.error(f"ملف السيرة الذاتية غير موجود: {cv_path}")
            print(f"❌ ملف السيرة الذاتية غير موجود: {cv_path}")
            return
        
        # إعداد المجدول
        self.setup_scheduler()
        
        # تشغيل المجدول
        if self.user_config.get('schedule_type') != 'immediate':
            logger.info("النظام يعمل في الخلفية...")
            print("✅ النظام يعمل في الخلفية")
            print("📊 لمراقبة النشاط، راجع ملف: cv_automation.log")
            print("⏹️ لإيقاف النظام، اضغط Ctrl+C")
            
            try:
                while True:
                    schedule.run_pending()
                    time.sleep(60)  # فحص كل دقيقة
            except KeyboardInterrupt:
                logger.info("تم إيقاف النظام بواسطة المستخدم")
                print("\n✅ تم إيقاف النظام")

def main():
    """الدالة الرئيسية"""
    print("🚀 نظام إرسال السيرة الذاتية الآلي")
    print("=" * 50)
    
    # التحقق من وجود ملف الإعدادات
    if not os.path.exists("user_config.json"):
        print("❌ ملف الإعدادات غير موجود!")
        print("🔧 يرجى تشغيل: python3 user_setup.py")
        return 1
    
    try:
        system = CVAutomationSystem()
        system.run()
        return 0
    except Exception as e:
        logger.error(f"خطأ في تشغيل النظام: {e}")
        print(f"❌ خطأ في تشغيل النظام: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 