# نظام ترشيح الممرضين (Nurse Recommendation System)

API لتوصية الممرضين حسب المدينة مع مراعاة التقييمات والخبرة.

## المتطلبات

- Python 3.9+
- FastAPI
- Pandas
- Joblib

## التثبيت المحلي

1. قم بتثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

2. قم بتشغيل التطبيق:
```bash
uvicorn main:app --reload
```

## النشر على Railway

1. قم بإنشاء حساب على [Railway](https://railway.app/)
2. قم بربط حسابك على GitHub
3. قم بإنشاء مشروع جديد واختر "Deploy from GitHub repo"
4. اختر المستودع الخاص بك
5. Railway سيقوم تلقائياً بنشر التطبيق

## استخدام API

### الحصول على الممرضين حسب المدينة
```
GET /nurses/{city}
```

مثال:
```
GET /nurses/cairo
```

## الوثائق

يمكنك الوصول إلى وثائق API التفاعلية على:
- Swagger UI: `/docs`
- ReDoc: `/redoc` 