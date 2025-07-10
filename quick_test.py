#!/usr/bin/env python3
"""
اختبار سريع للنظام
Quick Test for CV Automation System
"""

import os
import sys
import json

def test_system():
    """اختبار سريع للنظام"""
    print("🧪 اختبار سريع لنظام إرسال السيرة الذاتية")
    print("=" * 50)
    
    # فحص Python
    print(f"🐍 Python Version: {sys.version}")
    
    # فحص المكتبات المطلوبة
    required_packages = [
        'requests', 'beautifulsoup4', 'pandas', 
        'schedule', 'lxml', 'html5lib'
    ]
    
    print("\n📦 فحص المكتبات:")
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  مكتبات مفقودة: {', '.join(missing_packages)}")
        print("💡 تشغيل: pip install -r requirements_new.txt")
        return False
    
    # فحص الملفات
    print("\n📁 فحص الملفات:")
    required_files = [
        'user_setup.py', 'run_system.py', 
        'requirements_new.txt', 'دليل_التشغيل.md'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            return False
    
    # فحص ملفات PDF
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    if pdf_files:
        print(f"📄 ملفات PDF موجودة: {', '.join(pdf_files)}")
    else:
        print("⚠️  لا توجد ملفات PDF (ستحتاج لإضافة سيرتك الذاتية)")
    
    # فحص ملف الإعدادات
    if os.path.exists('user_config.json'):
        print("⚙️  ملف الإعدادات موجود")
        try:
            with open('user_config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"👤 المستخدم: {config.get('name', 'غير محدد')}")
            print(f"📧 البريد: {config.get('email', 'غير محدد')}")
            print(f"🏙️  المدن: {len(config.get('target_cities', []))}")
        except Exception as e:
            print(f"❌ خطأ في قراءة الإعدادات: {e}")
    else:
        print("⚠️  ملف الإعدادات غير موجود")
        print("💡 تشغيل: python3 user_setup.py")
    
    print("\n" + "=" * 50)
    print("✅ اختبار النظام مكتمل!")
    
    if not missing_packages:
        print("🚀 النظام جاهز للاستخدام")
        print("📖 راجع دليل_التشغيل.md للتعليمات المفصلة")
        return True
    else:
        print("⚠️  يرجى تثبيت المكتبات المفقودة أولاً")
        return False

if __name__ == "__main__":
    success = test_system()
    sys.exit(0 if success else 1) 