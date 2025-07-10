#!/usr/bin/env python3
"""
نظام إعداد المستخدم لإرسال السيرة الذاتية
User Setup System for CV Sending Automation
"""

import os
import sys
import json
import getpass
from datetime import datetime, time
import pytz

class UserSetup:
    """فئة إعداد المستخدم"""
    
    def __init__(self):
        self.user_data = {}
        self.config_file = "user_config.json"
        self.available_cities = [
            "الرياض", "جدة", "الدمام", "مكة المكرمة", "المدينة المنورة", "الطائف", "تبوك", "الأحساء", "بريدة", "خميس مشيط",
            "دبي", "أبوظبي", "الشارقة", "عجمان", "الفجيرة", "رأس الخيمة", "أم القيوين",
            "الكويت", "الأحمدي", "الفروانية", "الجهراء", "حولي", "مبارك الكبير",
            "عمان", "الزرقاء", "إربد", "الرصيفة", "الطفيلة", "الكرك", "معان", "العقبة",
            "مسقط", "صلالة", "نزوى", "صور", "صحار", "الرستاق", "البريمي"
        ]
        
    def welcome_message(self):
        """رسالة الترحيب"""
        print("=" * 80)
        print("🚀 مرحباً بك في نظام إرسال السيرة الذاتية الآلي")
        print("   Welcome to CV Sending Automation System")
        print("=" * 80)
        print()
        print("📋 هذا النظام سيساعدك في:")
        print("   • إرسال سيرتك الذاتية لشركات البرمجيات")
        print("   • البحث عن الوظائف في دول الخليج والأردن")
        print("   • إدارة عملية الإرسال تلقائياً")
        print()
        
    def get_user_info(self):
        """جمع معلومات المستخدم"""
        print("📝 من فضلك أدخل معلوماتك الشخصية:")
        print("-" * 50)
        
        # الاسم
        while True:
            name = input("🧑 الاسم الكامل (Full Name): ").strip()
            if name:
                self.user_data['name'] = name
                break
            print("❌ الاسم مطلوب!")
        
        # البريد الإلكتروني
        while True:
            email = input("📧 البريد الإلكتروني (Gmail): ").strip()
            if email and "@gmail.com" in email:
                self.user_data['email'] = email
                break
            print("❌ يجب أن يكون بريد Gmail صحيح!")
        
        # كلمة مرور التطبيق
        print("\n🔐 إعداد كلمة مرور التطبيق:")
        print("   لاستخدام Gmail، تحتاج إلى:")
        print("   1. تفعيل المصادقة الثنائية")
        print("   2. إنشاء كلمة مرور التطبيق من:")
        print("      https://myaccount.google.com/apppasswords")
        print()
        
        while True:
            password = getpass.getpass("🔑 كلمة مرور التطبيق (App Password): ").strip()
            if password:
                self.user_data['app_password'] = password
                break
            print("❌ كلمة مرور التطبيق مطلوبة!")
        
        # رقم الهاتف
        while True:
            phone = input("📱 رقم الهاتف (Phone Number): ").strip()
            if phone:
                self.user_data['phone'] = phone
                break
            print("❌ رقم الهاتف مطلوب!")
        
        # اسم ملف السيرة الذاتية
        print("\n📄 إعداد السيرة الذاتية:")
        cv_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
        
        if cv_files:
            print(f"📁 تم العثور على ملفات PDF: {', '.join(cv_files)}")
            if len(cv_files) == 1:
                cv_name = cv_files[0]
                print(f"✅ سيتم استخدام: {cv_name}")
            else:
                print("📋 اختر ملف السيرة الذاتية:")
                for i, file in enumerate(cv_files, 1):
                    print(f"   {i}. {file}")
                
                while True:
                    try:
                        choice = int(input("اختر الرقم: ")) - 1
                        cv_name = cv_files[choice]
                        break
                    except (ValueError, IndexError):
                        print("❌ اختيار غير صحيح!")
        else:
            cv_name = input("📝 اسم ملف السيرة الذاتية (CV filename): ").strip()
            if not cv_name:
                cv_name = "cv.pdf"
        
        self.user_data['cv_file'] = cv_name
        
        # التخصص/الوظيفة
        print("\n💼 التخصص المطلوب:")
        job_options = [
            "Software Project Manager",
            "Full Stack Developer", 
            "Frontend Developer",
            "Backend Developer",
            "Mobile App Developer",
            "DevOps Engineer",
            "Software Engineer",
            "Technical Lead",
            "Product Manager"
        ]
        
        print("📋 اختر التخصص أو اكتب تخصص مخصص:")
        for i, job in enumerate(job_options, 1):
            print(f"   {i}. {job}")
        print("   0. تخصص مخصص")
        
        while True:
            try:
                choice = input("اختر الرقم أو اكتب التخصص: ").strip()
                if choice.isdigit():
                    choice = int(choice)
                    if choice == 0:
                        job_title = input("اكتب التخصص: ").strip()
                        if job_title:
                            self.user_data['job_title'] = job_title
                            break
                    elif 1 <= choice <= len(job_options):
                        self.user_data['job_title'] = job_options[choice-1]
                        break
                    else:
                        print("❌ رقم غير صحيح!")
                else:
                    self.user_data['job_title'] = choice
                    break
            except ValueError:
                print("❌ إدخال غير صحيح!")
        
        # المدن المطلوبة
        self.get_target_cities()
        
        # توقيت التشغيل
        self.get_schedule_time()
        
    def get_target_cities(self):
        """اختيار المدن المطلوبة"""
        print("\n🏙️ المدن المطلوبة للبحث:")
        print("1. اختيار من قائمة المدن المتاحة")
        print("2. كتابة المدن يدوياً")
        print("3. جميع المدن المتاحة")
        
        while True:
            choice = input("اختر الطريقة (1-3): ").strip()
            if choice == "1":
                self.select_cities_from_list()
                break
            elif choice == "2":
                self.enter_cities_manually()
                break
            elif choice == "3":
                self.user_data['target_cities'] = self.available_cities
                print("✅ تم اختيار جميع المدن المتاحة")
                break
            else:
                print("❌ اختيار غير صحيح!")
    
    def select_cities_from_list(self):
        """اختيار المدن من القائمة"""
        print("\n📋 المدن المتاحة:")
        
        # تجميع المدن بالدول
        saudi_cities = self.available_cities[:10]
        uae_cities = self.available_cities[10:17]
        kuwait_cities = self.available_cities[17:22]
        jordan_cities = self.available_cities[22:30]
        oman_cities = self.available_cities[30:]
        
        print("\n🇸🇦 السعودية:")
        for i, city in enumerate(saudi_cities, 1):
            print(f"   {i}. {city}")
        
        print("\n🇦🇪 الإمارات:")
        for i, city in enumerate(uae_cities, 11):
            print(f"   {i}. {city}")
        
        print("\n🇰🇼 الكويت:")
        for i, city in enumerate(kuwait_cities, 18):
            print(f"   {i}. {city}")
        
        print("\n🇯🇴 الأردن:")
        for i, city in enumerate(jordan_cities, 23):
            print(f"   {i}. {city}")
        
        print("\n🇴🇲 عمان:")
        for i, city in enumerate(oman_cities, 31):
            print(f"   {i}. {city}")
        
        print("\nأدخل أرقام المدن مفصولة بفاصلة (مثال: 1,2,5,10)")
        print("أو اكتب 'all' لجميع المدن")
        
        while True:
            selection = input("اختر المدن: ").strip()
            if selection.lower() == 'all':
                self.user_data['target_cities'] = self.available_cities
                print("✅ تم اختيار جميع المدن")
                break
            
            try:
                indices = [int(x.strip()) for x in selection.split(',')]
                selected_cities = []
                for idx in indices:
                    if 1 <= idx <= len(self.available_cities):
                        selected_cities.append(self.available_cities[idx-1])
                    else:
                        print(f"❌ رقم غير صحيح: {idx}")
                        break
                else:
                    if selected_cities:
                        self.user_data['target_cities'] = selected_cities
                        print(f"✅ تم اختيار {len(selected_cities)} مدينة:")
                        for city in selected_cities:
                            print(f"   • {city}")
                        break
                    else:
                        print("❌ لم يتم اختيار أي مدينة!")
            except ValueError:
                print("❌ تنسيق غير صحيح! استخدم أرقام مفصولة بفاصلة")
    
    def enter_cities_manually(self):
        """كتابة المدن يدوياً"""
        print("\n✏️ اكتب المدن مفصولة بفاصلة:")
        print("مثال: الرياض, دبي, الكويت, عمان")
        
        while True:
            cities_input = input("المدن: ").strip()
            if cities_input:
                cities = [city.strip() for city in cities_input.split(',')]
                cities = [city for city in cities if city]  # إزالة الفراغات
                if cities:
                    self.user_data['target_cities'] = cities
                    print(f"✅ تم إدخال {len(cities)} مدينة:")
                    for city in cities:
                        print(f"   • {city}")
                    break
                else:
                    print("❌ لم يتم إدخال أي مدينة!")
            else:
                print("❌ يجب إدخال المدن!")
    
    def get_schedule_time(self):
        """تحديد توقيت التشغيل"""
        print("\n⏰ توقيت تشغيل النظام:")
        print("1. تشغيل فوري (الآن)")
        print("2. تشغيل يومي في وقت محدد")
        print("3. تشغيل أسبوعي")
        print("4. تشغيل شهري")
        
        while True:
            choice = input("اختر نوع التشغيل (1-4): ").strip()
            if choice == "1":
                self.user_data['schedule_type'] = 'immediate'
                print("✅ سيتم التشغيل فوراً")
                break
            elif choice == "2":
                self.get_daily_schedule()
                break
            elif choice == "3":
                self.get_weekly_schedule()
                break
            elif choice == "4":
                self.get_monthly_schedule()
                break
            else:
                print("❌ اختيار غير صحيح!")
    
    def get_daily_schedule(self):
        """تحديد التوقيت اليومي"""
        print("\n📅 التشغيل اليومي:")
        print("أدخل الوقت بصيغة 24 ساعة (مثال: 14:30)")
        
        while True:
            time_input = input("الوقت (HH:MM): ").strip()
            try:
                hour, minute = map(int, time_input.split(':'))
                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    self.user_data['schedule_type'] = 'daily'
                    self.user_data['schedule_time'] = f"{hour:02d}:{minute:02d}"
                    print(f"✅ سيتم التشغيل يومياً في الساعة {hour:02d}:{minute:02d}")
                    break
                else:
                    print("❌ وقت غير صحيح!")
            except ValueError:
                print("❌ تنسيق غير صحيح! استخدم HH:MM")
    
    def get_weekly_schedule(self):
        """تحديد التوقيت الأسبوعي"""
        days = ["الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"]
        
        print("\n📅 التشغيل الأسبوعي:")
        print("اختر يوم الأسبوع:")
        for i, day in enumerate(days, 1):
            print(f"   {i}. {day}")
        
        while True:
            try:
                day_choice = int(input("اختر اليوم (1-7): ")) - 1
                if 0 <= day_choice <= 6:
                    selected_day = days[day_choice]
                    break
                else:
                    print("❌ اختيار غير صحيح!")
            except ValueError:
                print("❌ يجب إدخال رقم!")
        
        while True:
            time_input = input("الوقت (HH:MM): ").strip()
            try:
                hour, minute = map(int, time_input.split(':'))
                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    self.user_data['schedule_type'] = 'weekly'
                    self.user_data['schedule_day'] = day_choice
                    self.user_data['schedule_time'] = f"{hour:02d}:{minute:02d}"
                    print(f"✅ سيتم التشغيل كل {selected_day} في الساعة {hour:02d}:{minute:02d}")
                    break
                else:
                    print("❌ وقت غير صحيح!")
            except ValueError:
                print("❌ تنسيق غير صحيح! استخدم HH:MM")
    
    def get_monthly_schedule(self):
        """تحديد التوقيت الشهري"""
        print("\n📅 التشغيل الشهري:")
        
        while True:
            try:
                day = int(input("اليوم من الشهر (1-28): "))
                if 1 <= day <= 28:
                    break
                else:
                    print("❌ اليوم يجب أن يكون بين 1 و 28!")
            except ValueError:
                print("❌ يجب إدخال رقم!")
        
        while True:
            time_input = input("الوقت (HH:MM): ").strip()
            try:
                hour, minute = map(int, time_input.split(':'))
                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    self.user_data['schedule_type'] = 'monthly'
                    self.user_data['schedule_day'] = day
                    self.user_data['schedule_time'] = f"{hour:02d}:{minute:02d}"
                    print(f"✅ سيتم التشغيل يوم {day} من كل شهر في الساعة {hour:02d}:{minute:02d}")
                    break
                else:
                    print("❌ وقت غير صحيح!")
            except ValueError:
                print("❌ تنسيق غير صحيح! استخدم HH:MM")
    
    def save_config(self):
        """حفظ الإعدادات"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_data, f, ensure_ascii=False, indent=2)
            print(f"\n✅ تم حفظ الإعدادات في {self.config_file}")
            return True
        except Exception as e:
            print(f"❌ خطأ في حفظ الإعدادات: {e}")
            return False
    
    def show_summary(self):
        """عرض ملخص الإعدادات"""
        print("\n" + "=" * 80)
        print("📋 ملخص الإعدادات")
        print("=" * 80)
        
        print(f"👤 الاسم: {self.user_data['name']}")
        print(f"📧 البريد الإلكتروني: {self.user_data['email']}")
        print(f"📱 الهاتف: {self.user_data['phone']}")
        print(f"📄 ملف السيرة الذاتية: {self.user_data['cv_file']}")
        print(f"💼 التخصص: {self.user_data['job_title']}")
        print(f"🏙️ عدد المدن: {len(self.user_data['target_cities'])}")
        
        if len(self.user_data['target_cities']) <= 10:
            print("   المدن المختارة:")
            for city in self.user_data['target_cities']:
                print(f"   • {city}")
        else:
            print("   المدن المختارة: (أول 10 مدن)")
            for city in self.user_data['target_cities'][:10]:
                print(f"   • {city}")
            print(f"   ... و {len(self.user_data['target_cities']) - 10} مدن أخرى")
        
        schedule_type = self.user_data['schedule_type']
        if schedule_type == 'immediate':
            print("⏰ التشغيل: فوري")
        elif schedule_type == 'daily':
            print(f"⏰ التشغيل: يومي في الساعة {self.user_data['schedule_time']}")
        elif schedule_type == 'weekly':
            days = ["الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"]
            day_name = days[self.user_data['schedule_day']]
            print(f"⏰ التشغيل: أسبوعي كل {day_name} في الساعة {self.user_data['schedule_time']}")
        elif schedule_type == 'monthly':
            print(f"⏰ التشغيل: شهري يوم {self.user_data['schedule_day']} في الساعة {self.user_data['schedule_time']}")
        
        print("\n✅ تم إعداد النظام بنجاح!")
        print("🚀 يمكنك الآن تشغيل النظام باستخدام: python3 run_system.py")
        print("=" * 80)
    
    def run(self):
        """تشغيل عملية الإعداد"""
        self.welcome_message()
        self.get_user_info()
        
        if self.save_config():
            self.show_summary()
            return True
        else:
            print("❌ فشل في حفظ الإعدادات!")
            return False

def main():
    """الدالة الرئيسية"""
    setup = UserSetup()
    success = setup.run()
    
    if success:
        print("\n🎉 تم الإعداد بنجاح!")
        print("📖 راجع ملف 'دليل_التشغيل.md' للحصول على تعليمات مفصلة")
        return 0
    else:
        print("\n❌ فشل في الإعداد!")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 