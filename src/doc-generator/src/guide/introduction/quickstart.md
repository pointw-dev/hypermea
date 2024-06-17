# Getting Started

<tabs>
<tab name="Python">

```python
api = Api()
api.add_headers({
    'Cache-control': 'no-cache',
    'Accept-language': 'en-CA, en;q=0.9, fr-CA;q=0.8, fr;q=0.7',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIiwiaWF0IjoyfQ.nMoAK-oiZTdVT0CcGhgS5yCscaNSf49BYFR3DiGT3tM'
})
```
</tab>

<tab name="JavaScript">

```javascript
const api = new Api()
api.addHeaders({
    'Cache-control': 'no-cache',
    'Accept-language': 'en-CA, en;q=0.9, fr-CA;q=0.8, fr;q=0.7',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIiwiaWF0IjoyfQ.nMoAK-oiZTdVT0CcGhgS5yCscaNSf49BYFR3DiGT3tM'
})
```
</tab>

</tabs>


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
