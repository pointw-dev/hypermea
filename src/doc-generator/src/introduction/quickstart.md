# Getting Started

Install hypermea into your Python virtual environment:

```bash
pip install hypermea
```

Create your API.  For example, to create a service named `order-processing`:

```bash
hy api create order-processing
```

This creates the following project folders and files:

```text
/order-processing
│   hypermea_service.py
│   requirements.txt
│   run.py
│   settings.py
│   _env.conf
│   
├───affordances
│       __init__.py
│       
├───configuration
│       api_settings.py
│       hypermea_settings.py
│       __init__.py
│       
├───domain
│       customers.py
│       orders.py
│       _common.py
│       _settings.py
│       __init__.py
│       
└───hooks
        customers.py
        orders.py
        _error_handlers.py
        _gateway.py
        _logs.py
        _settings.py
```

That's 23 files and almost a thousand lines of code that you do not have to type, ready for you to customize as you require.  This is just the tip of the iceberg.  

<!-- <comments-section repo="pointw-dev/hypermea" repoId="R_kgDOJxUXjg" category="General" categoryId="DIC_kwDOJxUXjs4CoFRU" /> -->
